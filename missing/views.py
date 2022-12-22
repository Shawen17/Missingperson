from django.forms import utils
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import MissingpersonForm,SignupForm,Profileform,ContactUsForm,EditProfileForm
from .models import ContactUs, Missingperson,Profile
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from Blog.models import Blog
from django.core.exceptions import ValidationError


def validate_number(value):
    if len(value)!= 11 or value[0]!=0:
        raise ValidationError('%s phone number incorrect' % value)    

def home(request):
    missings = Missingperson.objects.filter( datefound__isnull = True).order_by('-created')[:5]
    return render(request,'missing/home.html',{'missings':missings})

def about(request):
    return render(request,'missing/about.html')

def terms(request):
    return render(request,'missing/terms.html')

@login_required
def edit_user(request,user_id):
    user = User.objects.get(pk=user_id)
    user_form=Profileform(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Profileform, fields=('firstname','lastname','email','sex','profile_pic','bio'))
    formset = ProfileInlineFormset(instance=user)

    if  request.user.id == user.id:
        if request.method == "POST":
            user_form = Profileform(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return render(request,'missing/missingpage.html')

            return render(request, "missing/account_update.html", {
            "noodle": user_id,
            "noodle_form": user_form,
            "formset": formset})
        else:
            raise PermissionDenied

def missingperson(request):
    blogs= Blog.objects.order_by('-id')
    missings = Missingperson.objects.filter(datefound__isnull = True).order_by('-created')
    title=[i.title for i in blogs]
    blog_id=[i.id for i in blogs]
    missing_image = [i.image for i in missings]
    missing_firstname = [i.first_name for i in missings]
    missing_lastname = [i.last_name for i in missings]
    contact_person=[i.contact_person for i in missings]
    contact_number=[i.contact_number for i in missings]
    if len(missing_image)>len(title):
        w=len(missing_image)-len(title)
        g=[9]*w
        b=['...']*w
        title.extend(b)
        blog_id.extend(g)
        
    zipped_data=zip(blog_id,title,missing_firstname,missing_lastname,missing_image,contact_person,contact_number)
    return render(request,'missing/missingpage.html',{'zipped_data':zipped_data})

def foundperson(request):
    
    founds = Missingperson.objects.filter(datefound__isnull = False).order_by('-datefound')
    return render(request,'missing/foundperson.html',{'founds':founds})



def update_user_data(user):
    Profile.objects.create(user=user, defaults={'firstname': user.profile.firstname,'lastname': user.profile.lastname})
 




def signupuser(request):
    
    if request.method == 'POST':
        form = SignupForm()
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'missing/signupuser.html',{'form':form,'error':'Username Taken'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'missing/signupuser.html',{'form':form,'error':'Email Taken'})
            else:
                form = SignupForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()
                    user.profile.firstname=form.cleaned_data.get('firstname')
                    user.profile.lastname=form.cleaned_data.get('lastname')
                    user.profile.email=form.cleaned_data.get('email')
                    user.save()
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password1')
                    user= authenticate(username=username,password=password)
                    login(request,user)
                    return redirect('user_account')
                else:
                    form = SignupForm()
                    return render(request, 'missing/signupuser.html',{'form':form,'error':'form is invalid'})
        else:
            return render(request, 'missing/signupuser.html',{'form':form,'error':'Password does not match'})
    else:
        form = SignupForm()
        return render(request, 'missing/signupuser.html',{'form':form})

@login_required(login_url='/login/')
def createmissing(request):
    
    if request.method == 'GET':
        return render(request, 'missing/createmissing.html', {'form':MissingpersonForm()})
    else:
        form = MissingpersonForm(request.POST,request.FILES)
        if form.is_valid():
            newmissing = form.save(commit = False)
            newmissing.user = request.user
            newmissing.save()
            return redirect('missingperson')
        else:
            return render(request,'missing/createmissing.html',{'form':form,'error':'something went wrong'})
            
        #return render(request, 'missing/createmissing.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'missing/loginuser.html', {'form':AuthenticationForm()})
    else:
        user= authenticate(request, username=request.POST['username'],password=request.POST['password']) 
        if user is None:
             return render(request, 'missing/loginuser.html', {'form':AuthenticationForm(),'error':'Username or Password incorrect'})
        else:
            login(request,user)
            return redirect('user_account')
                

@login_required(login_url='/login/')
def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def found(request,missing_id):
    found = get_object_or_404(Missingperson,pk = missing_id,user=request.user)
    if request.method == 'POST':
        found.datefound = timezone.now()
        found.save()
        return redirect('user_account')

@login_required(login_url='/login/')  
def viewmissing(request,missing_id):
    view = get_object_or_404(Missingperson,pk = missing_id,user=request.user)
    if request.method == 'GET':
        form = MissingpersonForm(instance=view)
        return render (request, 'missing/viewmissing.html',{'view':view,'form':form})
    else:
        form = MissingpersonForm(request.POST,instance=view)
        form.save()
        return redirect('missingperson')

@login_required(login_url='/login/')
def deletemissing(request,missing_id):
    view = get_object_or_404(Missingperson,user=request.user,pk=missing_id)
    if request.method == 'POST':
        view.delete()
        return redirect('missingperson')

@login_required(login_url='/login/')
def user_account(request):
    user = request.user
    missings = Missingperson.objects.filter(user=request.user, datefound__isnull = True)
    mis_count = Missingperson.objects.filter(user=request.user, datefound__isnull = True).count
    return render(request,'missing/user_account.html',{'missings':missings,'user':user,'mis_count':mis_count})

@login_required(login_url='/login/')
def edit_profile(request):
    user=request.user.profile
    if request.method == 'GET':
        profile_form= Profileform(instance=user)
        return render (request, 'missing/account_update.html',{'user':user, 'profile_form':profile_form})
    else:
        profile_form = Profileform(request.POST,request.FILES,instance=user)
        if  profile_form.is_valid():
            custom_form=profile_form.save(commit=False)
            custom_form.user=request.user
            custom_form.save()
            return redirect('user_account')
        else:
            return render(request,'missing/account_update.html',{'profile_form':profile_form,'error':'info not valid'})


def policy(request):
    return render(request,'missing/policy.html')

def contact(request):
    
    if request.method=='POST':
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('home')
    else:
        contact_form=ContactUsForm()
        return render(request,'missing/contact.html',{'contact_form':contact_form})
