from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, DriverProfileForm,TripPlanForm
from .models import Driver_profile,TripPlan
from rider.models import Rider_profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction

# Create your views here.
def driver(request):
  user = User.objects.get(username = request.user.username)
  profile = Driver_profile.objects.get(user =user)
  riders = Rider_profile.objects.all()
  if request.method == 'POST':
    trip_form = TripPlanForm(request.POST)
    if trip_form.is_valid():
      trip_plan= TripPlan(driver_profile = request.user.driver_profile, current_location = request.POST['current_location'],destination = request.POST['destination'])
      trip_plan.save()
      print('success')
      return redirect(reverse('drivers:driver'))
  else:
    trip_form = TripPlanForm()
  return render(request, 'drivers/driver.html',{"profile": profile, "riders": riders, "trip_form":trip_form})

@transaction.atomic
def update_profile(request,username):
  user = User.objects.get(username = username)
  if request.method == 'POST':
    user_form = UserForm(request.POST, instance = request.user)
    profile_form = DriverProfileForm(request.POST, instance =request.user.driver_profile, files = request.FILES)
    if profile_form.is_valid() and user_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, ('Your profile was successfully updated!'))
      return redirect(reverse('drivers:profile', kwargs = {'username': request.user.username}))
    else:
      messages.error(request, ('Please correct the error below.'))

  else:
    user_form = UserForm(instance = request.user)
    profile_form = DriverProfileForm(instance = request.user.driver_profile)
  return render(request, 'drivers/profiles/profile_form.html', {"user_form":user_form, "profile_form":profile_form})

@login_required(login_url='/accounts/login')
def profile(request, username):
  user = User.objects.get(username =username)
  if not user:
    return redirect('driver')
  profile = Driver_profile.objects.get(user =user)
  print(profile.profile_pic)

  title = f"{user.username}"

  return render(request, 'drivers/profiles/profile.html', {"title":title, "user":user, "profile": profile})


def rider_profile(request,rider_profile_id):
  user= User.objects.get(id = rider_profile_id)
  if user:
    rider_profile = Rider_profile.objects.get(user=user)
  return render(request,'drivers/rider_profile.html',{"rider_profile": rider_profile})
