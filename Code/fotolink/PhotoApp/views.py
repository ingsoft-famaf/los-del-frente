from django.views.generic import ListView, CreateView
from django.views.generic import DetailView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PhotoForm
from .models import Photo, Place


class PhotoDelete(DeleteView):
    """
    Vista de eliminacion de una foto para uso de django. Hereda de
    django.views.generic.DeleteView
    """
    model = Photo
    template_name = 'PhotoApp/photo_delete.html'
    success_url = '/upload/'


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
        return reverse('photos:delete', kwargs={'pk': self.object.pk})


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

    '''
    Filtrar fotos. Una primera aproximacion al problema de buscar foto
    de acuerdo a ciertos parametros. Propongo:
    1- nombre de lugar contiene 'string':
        place_id=Place.objects.filter(placeName__contains='string')[0].id
        Mal: solo te da el primer resultado del conjunto de lugares cuyos
        nombres contienen 'string'.
    2- Por fecha y hora:
        En el ejemplo estan todas las fotos de julio entre las 8am y 6pm
    3- Fecha, hora y lugar
        Concatenar los filters.
    Manejar excepcion de empty queryset. No hay una forma mejor de hacer esto?
    Inputs del usuario...

    '''
    def get_queryset(self):
        '''
        if self.request.method=='POST':
            form = PhotoForm(self.request.POST)
            if form.is_valid():
                picPlace = form.cleaned_data['place']
                #picDate= form.cleaned_data['date']
                #picTime=form.cleaned_data['time']
        '''
        print "filtering"
        print self.request.GET
        picPlace = self.request.GET.get('place','')
        qset = super(PhotoList, self).get_queryset()
        return qset.filter(place=Place.objects.filter(placeName__contains=picPlace))
