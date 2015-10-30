from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.views.generic import FormView, DetailView, DeleteView
from .models import Photo
from .forms import PhotoForm
from django.core.urlresolvers import reverse
# Create your views here.

class PhotoDelete(DeleteView):
    model = Photo
    template_name = 'PhotoApp/photo_delete.html'
    success_url = '/upload/'

class PhotoDetail(DetailView):
    model = Photo
    template_name = 'PhotoApp/photo_detail.html'

class PhotoUpload(CreateView):
    template_name = 'PhotoApp/photo_form.html'
    form_class = PhotoForm
#    success_url = '/photos/'

    def get_success_url(self):
        return reverse ('photos:photodelete', kwargs={'pk': self.object.pk})

class PhotoList(ListView):
    model = Photo
    # paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data()
        return context
