from django.forms.models import ALL_FIELDS
from .models import Missingperson, Profile,ContactUs,states
from django.forms import ModelForm, fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Again'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    firstname = forms.CharField(max_length= 100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    lastname = forms.CharField(max_length= 100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    username = forms.CharField(max_length= 200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    
    class Meta:
        model = User
        fields = ('firstname','lastname','username','email','password1','password2')

    
class MissingpersonForm(ModelForm):
    
    first_name= forms.CharField(label='First Name',widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(label='Last Name',widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    nickname = forms.CharField(required=False,label='Nickname',widget=forms.TextInput(attrs={'placeholder':'Nickname'}))
    lastlocation = forms.CharField(label='Last Location')
    contact_person = forms.CharField( label='Contact Person',required=False)
    contact_number= forms.IntegerField()
    class Meta:
        model = Missingperson
        fields = ['first_name','last_name','nickname','image','sex','state','lastlocation','contact_person','contact_number']

   
        
class Profileform(ModelForm):
    
    firstname = forms.CharField(max_length= 100)
    lastname = forms.CharField(max_length= 100)
    email = forms.EmailField(max_length=100)
    class Meta:
        model = Profile
        fields = ('firstname','lastname','email','sex','profile_pic','bio')

    



class EditProfileForm(ModelForm):
    class Meta:
        model=User
        fields = ('username','email')        

    '''def save(self,commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.firstname = self.cleaned_data["firstname"]
        user.lastname = self.cleaned_data["lastname"]
        user.email = self.cleaned_data["email"]
        #user.username = "%s.%s" %(self.cleaned_data["firstname"],self.cleaned_data["lastname"])
        user.username = user.email
        
        if commit:
            user.save()
        return user'''

class ContactUsForm(ModelForm):
    
    class Meta:
        model= ContactUs
        fields = ('email','subject','body')
    

