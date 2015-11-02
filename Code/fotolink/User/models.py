from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Perfil(models.Model):
    usuario = models.OneToOneField(User, null = True)
    nombre = models.CharField(max_length=30)
    edad = models.IntegerField()
    residencia = models.CharField(max_length=40)
    mail = models.EmailField(max_length=70)
    facebook = models.URLField(max_length=60)
    web = models.URLField(max_length=200)
    avatar = ProcessedImageField(upload_to='avatars',
                                  null = True,
                                  processors=[ResizeToFill(300, 300)],
                                  format='JPEG',
                                  options= {'quality':90})

    def image_tag(self):
        return u'<img src="%s" alt= "404"/>' % self.avatar.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __string__ (self):
        return str(nombre)
