from django.contrib import admin
from .models import Photo, Place
# Register your models here.

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('picture','dateTime','place','image_tag')

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('placeName',)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Place, PlaceAdmin)
