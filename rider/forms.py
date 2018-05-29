from django import forms
from .models import Rider_profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Rider_profile
    fields = ('bio', 'location','profile_pic', 'phone_number')
