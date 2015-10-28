from django.conf.urls import include, url
from PhotoApp.views import PhotoList, PhotoUpload

urlpatterns = [
    url(r'^photos/', PhotoList.as_view(), name='photolist'),
    url(r'^upload/', PhotoUpload.as_view(), name='photoupload'),
] 
