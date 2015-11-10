from django.views.generic import ListView, CreateView
from django.views.generic import FormView, DetailView, DeleteView
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PhotoForm
from .models import Photo



class CancelUpload(DeleteView):
    model = Photo
    template_name = 'PhotoApp/cancel_upload.html'
    success_url = '/upload/'

class PhotoDelete(DeleteView):
    """
    Vista de eliminacion de una foto para uso de django. Hereda de
    django.views.generic.DeleteView
    """
    model = Photo
    template_name = 'PhotoApp/photo_delete.html'
    success_url = '/photos/'


class PhotoDetail(DetailView):
    """
    Vista de detalle de una foto para uso de django.Requiere login previo.
    Hereda de django.views.generic.DetailView
    """
    model = Photo
    template_name = 'PhotoApp/photo_detail.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo de salida de la vista que llama a su superclase. Requiere login

        :param request: http request
        :returns: http response
        """ 
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class PhotoUpload(CreateView):
    """
    Vista para subir una nueva foto, para uso de django. Requiere login previo.
    Hereda de django.views.generic.CreateView
    """
    template_name = 'PhotoApp/photo_form.html'
    form_class = PhotoForm

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        """
        Metodo de salida de la vista que llama a su superclase. Requiere login

        :param request: http request
        :returns: http response
        """
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Retorna un html para confirmar el subir una foto dado un primarykey
        """
        return reverse('photos:cancelupload', kwargs={'pk': self.object.pk})


class PhotoList(ListView):
    """
    Vista para listar fotos disponibles, para uso de django. Requiere login
    previo. Hereda de django.views.generic.ListView
    """
    model = Photo

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
        context = super(PhotoList, self).get_context_data()
        return context
