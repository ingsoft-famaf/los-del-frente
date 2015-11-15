from django.contrib import admin
from .models import Perfil, Friendship
from django.contrib.auth.models import Permission


class ProfileAdmin(admin.ModelAdmin):
    """
    Clase para manejo de un modelo django, desde la interfaz de admin, tambien
    de django. Hereda de django.contrib.admin.ModelAdmin
    """
    list_display = ('nombre', 'edad', 'residencia', 'mail', 'facebook',
                    'web', 'image_tag', 'usuario')


class FriendshipAdmin(admin.ModelAdmin):
    '''
    '''
    list_display = ('id', 'from_user', 'to_user')


class PermissionAdmin(admin.ModelAdmin):
    '''
    Clase para ver los permisos actuales que tiene la aplicacion
    En nuestro caso sirve para ver si hay problemas en la creacion del permiso
    'Can_see'
    '''
    model = Permission
    list_display = ('name',)

admin.site.register(Perfil, ProfileAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Permission, PermissionAdmin)
