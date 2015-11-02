from django.conf.urls import include, url
from PhotoApp.views import PhotoList, PhotoUpload, PhotoDetail, PhotoDelete

urlpatterns = [
    url(r'^photos/', PhotoList.as_view(), name='photolist'),
    url(r'^upload/', PhotoUpload.as_view(), name='photoupload'),
    url(r'^/(?P<pk>[0-9]+)/$', PhotoDetail.as_view(), name='photodetail'),
    url(r'^/delete/(?P<pk>[0-9]+)/$',PhotoDelete.as_view(), name='photodelete'),
] 
