from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import views
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Perfil, Friendship, FriendshipInvitation, friend_set_for
from .forms import ProfileForm
from forms import UserCreationForm


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
    Vista de mi Perfil de usuario.Hereda de django.views.generic.DetailView
    Requiere estar logueado en el sistema.

    Overrides: dispatch, get_object
    """
    model = Perfil
    template_name = 'User/profile.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo agregado para requerir login con decorador.

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
    """
    Clase para mostrar la lista de amistades del usuario
    """

    model = Friendship
    template_name = 'User/link_list.html'

    def get_queryset(self):

        ActualUser = get_object_or_404(User, username=self.request.user)
        return friend_set_for(ActualUser)


class InviteList(ListView):
    """
    Aqui se listan todas las solicitudes de amistad pendientes
    del usuario, dandole tambien la posibilidad de aceptarlas o
    rechazarlas.
    """

    model = FriendshipInvitation
    template_name = 'User/invite_list.html'

    def get_queryset(self):

        qset = super(InviteList, self).get_queryset()
        ActualUser = get_object_or_404(User, username=self.request.user)
        accept = self.request.GET.get('Accept', '')
        decline = self.request.GET.get('Decline', '')
        frReqId = self.request.GET.get('requestID', '')

        if accept != '':
            Invitation = FriendshipInvitation.objects.get(id=frReqId)
            # poner aca metodo para decirle al 'aceptado' que somos amiguitos
            Invitation.accept()
        if decline != '':
            Invitation = FriendshipInvitation.objects.get(id=frReqId)
            Invitation.decline()
        return qset.filter(to_user=ActualUser).filter(status="0")



class PeopleList(ListView):
    """
    Permite buscar amigos en la red.
    """
    model = Perfil
    template_name = 'User/people_list.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo agregado para requerir login con decorador.

        :param request: http request
        :returns: http response
        """
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''
        Filtra segun el formulario enviado por el usuario y retorna una lista
        de objetos con las caracteristicas adecuadas.
        En este caso filtra coincidencias en nombre, usuario, mail empezando
        con el argumento enviado por el usuario
        '''
        qName = self.request.GET.get('people', '')
        qset = super(PeopleList, self).get_queryset()
        if qName != "":
            qset = qset.filter(usuario__username__startswith=qName) | qset.filter(mail__startswith=qName) | qset.filter(nombre__startswith=qName)
        else:
            return []
        return qset


class OthersProfile(DetailView):
    """
    Vista de un Perfil de otro usuario con restricciones si no son amigos.
    Hereda de django.views.generic.DetailView.
    Requiere estar logueado en el sistema.
    """
    model = Perfil
    template_name = 'User/othersprofile.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Disparador selectivo segun si es mi perfil, si es el de un amigo o si
        es hacia un contacto desconocido.

        :param request: http request
        :returns: http response
        """
        userToShow = User.objects.get(pk=kwargs['pk'])
        actualUser = self.request.user
        ct = ContentType.objects.get_for_model(model=Perfil)
        perm = Permission.objects.get_or_create(codename='Can_see',
                                                name='Can see pr_profile',
                                                content_type=ct)
        if (int(request.user.pk) == int(kwargs['pk'])):
            return HttpResponseRedirect("/accounts/profile")
        elif(userToShow in friend_set_for(actualUser)):
            perm = Permission.objects.get(codename='Can_see')
            actualUser.user_permissions.add(perm)
            return super(self.__class__, self).dispatch(request,
                                                        *args,
                                                        **kwargs)
        else:
            perm = Permission.objects.get(codename='Can_see')
            actualUser.user_permissions.remove(perm)
            return super(self.__class__, self).dispatch(request,
                                                        *args,
                                                        **kwargs)
