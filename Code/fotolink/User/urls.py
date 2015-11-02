from django.conf.urls import url
from User.views import Register, ProfileEdit,ProfileDetail, ProfileCreate
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^register/', Register.as_view(), name='registro'),
    url(r'^reg_ok/', TemplateView.as_view(template_name='User/reg_ok.html')),
    url('^createprofile/$', ProfileCreate.as_view(), name='createprofile'),
    url(r'^profile/(?P<pk>[-\w]+)/$', ProfileDetail.as_view(), name='profile'),
    url(r'^profile_edit/(?P<pk>[-\w]+)/$', ProfileEdit.as_view(), name='editprofile'),
    url(r'^edit_ok/', TemplateView.as_view(template_name='User/edit_ok.html')),
]
