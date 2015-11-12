from django.contrib import admin
from .models import Photo, Place, Notification


class PhotoAdmin(admin.ModelAdmin):
    """
    Clase para manejo del modelo Photo django, desde la interfaz de admin,
    tambien de django. Hereda de django.contrib.admin.ModelAdmin
    """
    list_display = ('picture', 'date', 'time', 'place', 'image_tag')


class PlaceAdmin(admin.ModelAdmin):
    """
    Clase para manejo del modelo Photo django, desde la interfaz de admin,
    tambien de django. Hereda de django.contrib.admin.ModelAdmin
    """
    list_display = ('placeName',)


class NotificationAdmin(admin.ModelAdmin):
    """
    Clase para manejo del modelo Notification, desde la interfaz de admin,
    tambien de django. Hereda de django.contrib.admin.ModelAdmin
    """
    list_display = ('sender','receiver','text',)


admin.site.register(Notification, NotificationAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Place, PlaceAdmin)
