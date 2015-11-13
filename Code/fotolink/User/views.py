from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic import DetailView, TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import views
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from forms import UserCreationForm, ProfileForm
from .models import Perfil
from .forms import ProfileForm


class Register(CreateView):
    """
    Vista de registro de usuario para uso de django. Posee la funcionalidad
    de crear nuevos usuarios con sus passwords. Hereda de
    django.views.generic.CreateView
    """
    template_name = 'User/register.html'
    form_class = UserCreationForm
    success_url = '/login/'


class ProfileDetail(DetailView):
    """
    Vista de un Perfil de un usuario.Hereda de django.views.generic.DetailView
    Requiere estar logueado en el sistema.

    Overrides: dispatch, get_object
    """
    model = Perfil
    template_name = 'User/profile.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo de salida de la vista que llama a su superclase. Requiere login

        :param request: http request
        :returns: http response
        """
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Retorna un objeto de tipo Perfil del usuario que hace el pedido.
        Levanta excepcion Http404.
        """
        ActualUser = get_object_or_404(User, username=self.request.user)
        return get_object_or_404(Perfil, usuario=ActualUser)


class ProfileEdit(UpdateView):
    """
    Clase que implementa la vista de actualizacion de un perfil de usuario.
    Requiere login y es clase hija de UpdateView. Hereda de
    django.views.generic.UpdateView

    Overrides: dispatch, get_object, form_valid
    """
    template_name = 'User/profile_edit.html'
    model = Perfil
    form_class = ProfileForm
    success_url = '/edit_ok/'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo de salida de la vista que llama a su superclase. Requiere login.

        :param request: http request
        :returns: http response
        """
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Devuelve un objeto Perfil del usuario que hace el pedido
        Levanta excepcion Http404.
        """
        ActualUser = get_object_or_404(User, username=self.request.user)
        return get_object_or_404(Perfil, usuario=ActualUser)

    def form_valid(self, form):
        """
        Valida un formulario y guarda el registro recibido como parametro
        sobre el usuario logueado.

        :param form: formulario html con datos de un Perfil
        :returns: HttpResponseRedirect: objeto con la direccion de redireccion
        """
        usuario = form.save(commit=False)
        usuario.usuario = User.objects.get(username=self.request.user)
        usuario.save()
        return HttpResponseRedirect(self.get_success_url())


class LinkList(ListView):

    model = Perfil
    template_name = 'User/link_list.html'
    queryset = Perfil.objects.prefetch_related('vinculos')

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo de salida de la vista que llama a su superclase. Requiere login

        :param request: http request
        :returns: http response
        """
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Retorna el contexto de todas las fotos en PhotoList
        """
        context = super(LinkList, self).get_context_data()
        return context
