from django.contrib import admin
from .models import Perfil

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nombre','edad','residencia','mail','facebook','web','image_tag')

admin.site.register(Perfil, ProfileAdmin)
