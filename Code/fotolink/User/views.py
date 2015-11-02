from forms import UserCreationForm, ProfileForm
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import views
from .models import Perfil
from .forms import ProfileForm


class Register(CreateView):
    template_name = 'User/register.html'
    form_class = UserCreationForm
    success_url = '/reg_ok/'

class ProfileCreate(CreateView):
    model = Perfil
    form_class = ProfileForm
    template_name = 'User/profile_create.html'

    #Esto no estaria andando
    def form_valid(self, form):
        self.object.usuario = self.request.pk
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ProfileDetail(DetailView):
    model = Perfil
    template_name = 'User/profile.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        return context

class ProfileEdit(UpdateView):
    template_name = 'User/profile_edit.html'
    model = Perfil
    form_class = ProfileForm
    success_url = '/edit_ok/'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        return context
