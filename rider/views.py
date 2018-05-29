from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm,ProfileForm
from .models import Rider_profile
from drivers.models import Driver_profile,TripPlan,Booking
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def rider(request):
  user = User.objects.get(username = request.user.username)
  profile = Rider_profile.objects.get(user =user)
  drivers = Driver_profile.objects.all()
  return render(request, 'rider/rider.html', {"profile": profile, "drivers":drivers})


def update_profile(request,username):
  user = User.objects.get(username = username)
  if request.method == 'POST':
    user_form = UserForm(request.POST, instance = request.user)
    profile_form = ProfileForm(request.POST, instance =request.user.rider_profile, files = request.FILES)
    if user_form.is_valid() and profile_form.is_valid():
      print('master')
      user_form.save()
      profile_form.save()
      messages.success(request, ('Your profile was successfully updated!'))
      return redirect(reverse('rider:profile', kwargs = {'username': request.user.username}))
    else:
      messages.error(request, ('Please correct the error below.'))

  else:
    user_form = UserForm(instance = request.user)
    profile_form = ProfileForm(instance = request.user.rider_profile)
  return render(request, 'rider/profiles/profile_form.html', {"user_form":user_form, "profile_form":profile_form})

@login_required
def profile(request, username):
  user = User.objects.get(username =username)
  if not user:
    return redirect('rider')
  profiles = Rider_profile.objects.get(user =user)

  title = f"{user.username}"

  return render(request, 'rider/profiles/profile.html', {"title":title, "user":user, "profiles": profiles})


#Rider sees a particular driver's profile
def driver_profile(request,driver_profile_id,trip_plan_id):
  user= User.objects.get(id = driver_profile_id)
  if user:
    driver_profile = Driver_profile.objects.get(user=user)
    trip_plan = TripPlan.objects.get(id = trip_plan_id)
    existing_bookings = Booking.objects.filter(trip_plan =trip_plan.id)
    if len(existing_bookings) < trip_plan.driver_profile.car_capacity:
      seats_left = trip_plan.driver_profile.car_capacity - len(existing_bookings)
      return render(request,'rider/driver_profile.html',{'driver_profile': driver_profile,"seats_left":seats_left,"trip_plan":trip_plan})
    elif len(existing_bookings) == trip_plan.driver_profile.car_capacity:
      message = "this ride is fully booked"
      return render(request,'rider/driver_profile.html',{'driver_profile': driver_profile,"message":message})

def booking_seat(request, driver_profile_id):
  current_user = request.user

  rider_profile = Rider_profile.objects.get(user= current_user)

  found_profile = Driver_profile.objects.get(id = driver_profile_id)

  trip_plan = TripPlan.objects.get(driver_profile = found_profile)

  existing_bookings = Booking.objects.filter(trip_plan=trip_plan)

  if len(existing_bookings) < trip_plan.driver_profile.car_capacity:
    new_booking = Booking(rider_profile= rider_profile, trip_plan = trip_plan)

    new_booking.save()

    print(new_booking)

  elif len(existing_bookings) == trip_plan.driver_profile.car_capacity:
    return redirect(reverse('rider:driver_profile', kwargs={'driver_profile_id':Driver_profile.user.id}))
