from django.contrib import admin
from .models import Perfil, Friendship


class ProfileAdmin(admin.ModelAdmin):
    """
    Clase para manejo de un modelo django, desde la interfaz de admin, tambien
    de django. Hereda de django.contrib.admin.ModelAdmin
    """
    list_display = ('nombre', 'edad', 'residencia', 'mail', 'facebook',
                    'web', 'image_tag', 'usuario')

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user')

admin.site.register(Perfil, ProfileAdmin)
admin.site.register(Friendship, FriendshipAdmin)
