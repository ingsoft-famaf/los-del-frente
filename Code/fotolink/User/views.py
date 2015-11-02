from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# Para buscar objetos de tipo usuario generico
from django.shortcuts import get_object_or_404
# Para restricciones de acceso
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Para usuarios genericos
from forms import UserCreationForm, ProfileForm

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

    '''
    Este metodo sobreescribe el default obligando a estar logueado
    '''

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    '''
    Valida el formulario y completa el usuario con el usuario actual logueado.
    '''
    # AutoComplete form.usuario with actual logged in user
    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.usuario = User.objects.get(username=self.request.user)
        usuario.save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileDetail(DetailView):
    model = Perfil
    template_name = 'User/profile.html'

    '''
    Este metodo sobreescribe el default obligando a estar logueado
    '''
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    '''
    Devuelve un objeto Perfil que respecta a la relacion, uno a uno
    que hay entre el Usuario quien hace el pedido y su Perfil
    '''
    def get_object(self):
        ActualUser = get_object_or_404(User, username=self.request.user)
        return get_object_or_404(Perfil, usuario=ActualUser)


class ProfileEdit(UpdateView):
    template_name = 'User/profile_edit.html'
    model = Perfil
    form_class = ProfileForm
    success_url = '/edit_ok/'

    '''
    Este metodo sobreescribe el default obligando a estar logueado
    '''
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    '''
    Devuelve un objeto Perfil que respecta a la relacion, uno a uno
    que hay entre el Usuario quien hace el pedido y su Perfil
    '''
    def get_object(self):
        ActualUser = get_object_or_404(User, username=self.request.user)
        return get_object_or_404(Perfil, usuario=ActualUser)

    '''
    Valida el formulario y completa el usuario con el usuario actual logueado.
    '''
    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.usuario = User.objects.get(username=self.request.user)
        usuario.save()
        return HttpResponseRedirect(self.get_success_url())
