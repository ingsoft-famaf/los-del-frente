from forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import views
from User.models import Perfil


class Register(CreateView):
    template_name = 'User/register.html'
    form_class = UserCreationForm
    success_url = '/reg_ok/'

class Profile(CreateView):
    template_name = 'User/profile.html'
    model = Perfil
    form_class = HACERFORMULARIO
    success_url = '/reg_ok/'
