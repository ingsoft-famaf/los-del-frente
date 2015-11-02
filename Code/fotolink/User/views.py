from forms import UserCreationForm, ProfileForm
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import views
from django.contrib.auth.models import User
from .models import Perfil
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

class Register(CreateView):
    template_name = 'User/register.html'
    form_class = UserCreationForm
    success_url = '/reg_ok/'

class ProfileCreate(CreateView):
    model = Perfil
    form_class = ProfileForm
    template_name = 'User/profile_create.html'

    # AutoComplete form.usuario with actual logged in user
    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.usuario = User.objects.get(username=self.request.user)
        usuario.save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileDetail(DetailView):
    model = Perfil
    template_name = 'User/profile.html'

    def get_object(self):
        ActualUser = get_object_or_404(User, username=self.request.user)
        return get_object_or_404(Perfil, usuario=ActualUser)

class ProfileEdit(UpdateView):
    template_name = 'User/profile_edit.html'
    model = Perfil
    form_class = ProfileForm
    success_url = '/edit_ok/'

    def get_object(self):
        ActualUser = get_object_or_404(User, username=self.request.user)
        return get_object_or_404(Perfil, usuario=ActualUser)

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.usuario = User.objects.get(username=self.request.user)
        usuario.save()
        return HttpResponseRedirect(self.get_success_url())
