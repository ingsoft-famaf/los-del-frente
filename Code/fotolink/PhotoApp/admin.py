from django.contrib import admin
from .models import Photo, Place, Notification, Tag


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


class TagAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('photo', 'user', 'x_pos', 'y_pos', 'pk')


class NotificationAdmin(admin.ModelAdmin):
    """
    Clase para manejo del modelo Notification, desde la interfaz de admin,
    tambien de django. Hereda de django.contrib.admin.ModelAdmin
    """
    list_display = ('sender', 'receiver', 'text', 'dateTime', 'seen',
                    'notif_type')

admin.site.register(Tag, TagAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Place, PlaceAdmin)
