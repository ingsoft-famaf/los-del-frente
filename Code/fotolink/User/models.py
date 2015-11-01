from django.db import models


class Perfil(models.Model):
    nombre = models.CharField(max_length=30)
    edad = models.IntegerField()
    residencia = models.CharField(max_length=40)
    mail = models.EmailField(max_length=70)
    facebook = models.URLField(max_length=60)
    web = models.URLField(max_length=200)
    #foto_perfil = models.ImageField()
    es_moderador = models.BooleanField()
