from django.test import TestCase
from .forms import MissingpersonForm


data={'first_name':'johnson','last_name':'abu','nickname':'abubs','image':'car1.jpg','state':'ogun','lastlocation':'abule',
'contact_person':'anu','contact_number':'123456'}

f= MissingpersonForm(data)
f.is_valid()
