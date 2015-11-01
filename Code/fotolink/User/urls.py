from django.conf.urls import url
from User.views import Register, Profile
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^register/', Register.as_view(), name='registro'),
    url(r'^reg_ok/', TemplateView.as_view(template_name='User/reg_ok.html')),
    url(r'^perfil/(?P<pk>[-\w]+)/$', Profile.as_view(), name='perfil'),
]
