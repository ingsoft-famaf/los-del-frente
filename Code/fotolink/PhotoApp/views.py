from django.views.generic import ListView, CreateView
from django.views.generic import FormView, DetailView, DeleteView
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PhotoForm
from .models import Photo


class PhotoDelete(DeleteView):
    model = Photo
    template_name = 'PhotoApp/photo_delete.html'
    success_url = '/upload/'


class PhotoDetail(DetailView):
    model = Photo
    template_name = 'PhotoApp/photo_detail.html'
    '''
    Este metodo sobreescribe el default obligando a estar logueado
    '''
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class PhotoUpload(CreateView):
    template_name = 'PhotoApp/photo_form.html'
    form_class = PhotoForm

    '''
    Este metodo sobreescribe el default obligando a estar logueado
    '''
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('photos:delete', kwargs={'pk': self.object.pk})


class PhotoList(ListView):
    model = Photo

    '''
    Este metodo sobreescribe el default obligando a estar logueado
    '''
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data()
        return context
