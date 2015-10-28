from django.shortcuts import render
from django.views.generic import ListView, CreateView,FormView
from .models import Photo
from .forms import PhotoForm
# Create your views here.

class PhotoUpload(CreateView):
    template_name = 'PhotoApp/photo_form.html'
    form_class = PhotoForm
    success_url = '/upload/'

class PhotoList(ListView):
    model = Photo

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data()
        return context
