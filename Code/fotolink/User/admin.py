from django.contrib import admin
from .models import Perfil, Relationship


class ProfileAdmin(admin.ModelAdmin):
    """
    Clase para manejo de un modelo django, desde la interfaz de admin, tambien
    de django. Hereda de django.contrib.admin.ModelAdmin
    """
    list_display = ('nombre', 'edad', 'residencia', 'mail', 'facebook',
                    'web', 'image_tag', 'usuario')

admin.site.register(Perfil, ProfileAdmin)


class RelationshipInline(admin.StackedInline):
    model = Relationship
    fk_name = 'from_person'
