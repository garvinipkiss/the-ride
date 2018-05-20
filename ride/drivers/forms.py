from django import forms
from .models import Driver_profile,TripPlan
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name')

class DriverProfileForm(forms.ModelForm):
  class Meta:
    model = Driver_profile
    fields = ('bio', 'city','profile_pic', 'phone_number', 'car_image','car_capacity', 'car_number_plates', 'car_model','car_color', 'current_location','destination',)

class TripPlanForm(forms.ModelForm):
  class Meta:
    model = TripPlan
    fields = ('current_location','destination',)
