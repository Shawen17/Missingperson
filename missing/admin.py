from django.contrib import admin
from .models import Missingperson,Profile,ContactUs
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User



@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    list_display =('email','subject','body','date')
    ordering =('-date','subject',)
    search_fields = ('email','subject')




@admin.register(Missingperson)
class MissingpersonAdmin(ModelAdmin):
    list_display =('first_name','last_name','nickname','image','sex','created','datefound','state',
    'lastlocation','contact_person','contact_number')
    ordering = ('-created','sex',)
    search_fields=('state','first_name','last_name','sex')

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display =('firstname','lastname','email','sex','profile_pic','bio')


class ProfileInline(admin.StackedInline):
    model=Profile
    fk_name = 'user'
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
