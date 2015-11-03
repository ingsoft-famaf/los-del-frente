from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm
from .models import Perfil


class ProfileForm(ModelForm):
    """
    Clase ProfileForm para manejo en django de formularios a partir de un
    modelo dado. El modelo que implementa esta clase es User.models.Perfil
    Hereda de django.forms.ModelForm y posee una sublclase interna mediante
    la cual se instancia el modelo mencionado junto con sus campos.
    """
    class Meta:
        model = Perfil
        exclude = ('usuario',)
        fields = '__all__'
