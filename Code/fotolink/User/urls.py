from django.conf.urls import url
from User.views import Register, ProfileEdit, ProfileDetail, LinkList
from .views import PeopleList, OthersProfile
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^register/', Register.as_view(), name='registro'),
    url(r'^reg_ok/', TemplateView.as_view(template_name='User/reg_ok.html')),
    url(r'^accounts/profile/$', ProfileDetail.as_view(), name='profile'),
    url(r'^accounts/profile/edit/$', ProfileEdit.as_view(), name='edit'),
    url(r'^accounts/profile/links/$', LinkList.as_view(), name='vinculos'),
    url(r'^edit_ok/', TemplateView.as_view(template_name='User/edit_ok.html')),
    url(r'^$', ProfileDetail.as_view(), name='home'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', OthersProfile.as_view(), name='oprofile'),
    url(r'^people', PeopleList.as_view(), name='people')
]
