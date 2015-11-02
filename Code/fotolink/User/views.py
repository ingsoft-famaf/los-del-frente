from forms import UserCreationForm, ProfileForm
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import views
from User.models import Perfil


class Register(CreateView):
    template_name = 'User/register.html'
    form_class = UserCreationForm
    success_url = '/reg_ok/'

class Profile(UpdateView):
    template_name = 'User/profile.html'
    model = Perfil
    form_class = ProfileForm
    success_url = '/edit_ok/'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        return context
