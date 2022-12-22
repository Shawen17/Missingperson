from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def social_page(request):
    return render(request,'social/social_page.html')

def register(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'new account created: {username}')
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        else:
            messages.error(request,'account creation failed')
        return redirect('social:social_page')
    
    form = UserCreationForm()
    return render(request,'social/register.html',{'form':form})