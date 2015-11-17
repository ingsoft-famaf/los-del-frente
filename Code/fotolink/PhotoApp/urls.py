from django.conf.urls import include, url
from PhotoApp.views import PhotoList, PhotoUpload, PhotoDetail
from PhotoApp.views import PhotoDelete, CancelUpload, notifications, AddTag

urlpatterns = [
    url(r'^photos/', PhotoList.as_view(), name='list'),
    url(r'^upload/', PhotoUpload.as_view(), name='upload'),
    url(r'^/photos/(?P<pk>[0-9]+)/$', PhotoDetail.as_view(), name='detail'),
    url(r'^/delete/(?P<pk>[0-9]+)/$', PhotoDelete.as_view(), name='delete'),
    url(r'^/cancelupload/(?P<pk>[0-9]+)/$', CancelUpload.as_view(), name='cancelupload'),
    url(r'^notification', notifications, name='notifications'),
    url(r'^addtag', AddTag, name='addtag')
]
