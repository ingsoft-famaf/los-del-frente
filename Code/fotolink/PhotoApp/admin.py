from django.contrib import admin
from .models import Photo
# Register your models here.

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('picture','dateTime','place','image_tag')

admin.site.register(Photo, PhotoAdmin)
