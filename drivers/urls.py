from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

app_name = 'drivers'

urlpatterns = [
  url(r'^$',views.driver, name = 'driver'),
  url(r'^profile/(?P<username>[-_\w.]+)/$', views.profile, name='profile'),
  url(r'^profile/(?P<username>[-_\w.]+)/edit/$', views.update_profile, name='edit'),
  url(r'^rider_profile/(\d+)/$', views.rider_profile, name='rider_profile'),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
