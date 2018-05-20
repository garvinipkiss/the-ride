from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
# from drivers.models import Driver_profile


# Create your models here.
class Rider_profile(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  bio = models.TextField(max_length=200, blank =True)
  location = models.CharField(max_length = 50, blank =True)
  phone_number =models.IntegerField(blank = True, null = True)
  profile_pic = models.ImageField(upload_to = 'profile_pic/', blank=True, null= True)


  @receiver(post_save, sender = User)
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      Rider_profile.objects.create(user=instance)

  @receiver(post_save, sender = User)
  def save_user_profile(sender,instance, **kwargs):
    instance.rider_profile.save()
