from django import dispatch
from django.db import  models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import pandas as pd
from missingperson.settings import STATIC_ROOT


file_path = os.path.join(STATIC_ROOT,'missing\\state.xlsx')
df = pd.read_excel(file_path)
df1= zip(df.value,df.representation)
states=[]
for i,j in df1:
    states.append((i,j))


'''states = (
    ('lagos','Lagos'),
    ('ogun','Ogun'),
    ('oyo','Oyo'),
    ('osun','Osun')
)'''
com_list=(
    ('enquiry','Enquiry'),
    ('complaint','Complaint'),
    ('report','Report'),
    ('others','Others')
)


gender =(
    ('male','Male'),
    ('female','Female')
)

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    firstname = models.CharField(max_length=100,blank=True,default='')
    lastname = models.CharField(max_length=100,blank=True,default='')
    email =models.EmailField(max_length=150)
    sex=models.CharField(max_length=10,choices=gender,blank=True,default='')
    profile_pic = models.ImageField(upload_to='missing/images/',default='static/missing/car2.jpg')
    bio = models.TextField(blank=True,default='')

    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User,dispatch_uid='user.created')   
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



class Missingperson(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    nickname = models.CharField(max_length = 100,blank=True,null=True)
    image=models.ImageField(upload_to='missing/images/',default='missing/car2.jpg')
    sex= models.CharField(max_length=10,choices=gender)
    created = models.DateTimeField(auto_now_add=True)
    datefound = models.DateTimeField(null=True,blank=True)
    state = models.CharField(max_length=50,choices= states)
    lastlocation = models.CharField(max_length=200,blank=True,null=True)
    contact_person = models.CharField(max_length = 200,blank=True,null=True)
    contact_number = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}' 

    

class ContactUs(models.Model):
    email= models.EmailField(max_length=150)
    subject= models.CharField(max_length=20,choices=com_list)
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email