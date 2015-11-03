from django import forms
from .models import Photo


class PhotoForm(forms.ModelForm):
    """
    Clase PhotoForm para manejo en django de formularios a partir de un
    modelo dado. El modelo que implementa esta clase es User.models.Ptoto.
    Hereda de django.forms.ModelForm y posee una sublclase interna mediante
    la cual se instancia el modelo mencionado junto con sus campos.
    """
    class Meta:
        model = Photo
        fields = '__all__'
