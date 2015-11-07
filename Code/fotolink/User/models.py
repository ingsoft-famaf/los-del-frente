from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator


class Perfil(models.Model):
    """
    Clase Perfil que modela los datos visibles o no, de un usuario registrado.
    Hereda de django.db.models.Model y es para casi uso exclusivo de django.
    """
    usuario = models.OneToOneField(User, null=True)
    nombre = models.CharField(max_length=30, blank=True)
    edad = models.PositiveIntegerField(blank=True,
                                       null=True,
                                       validators=[MaxValueValidator(150)])
    edad_privacidad = models.BooleanField("privacidad", default=True)
    residencia = models.CharField(max_length=40, blank=True)
    residencia_privacidad = models.BooleanField("privacidad", default=True)
    mail = models.EmailField(max_length=70, blank=True)
    mail_privacidad = models.BooleanField("privacidad", default=True)
    facebook = models.URLField(max_length=60, blank=True)
    facebook_privacidad = models.BooleanField("privacidad", default=True)
    web = models.URLField(max_length=200, blank=True)
    web_privacidad = models.BooleanField("privacidad", default=True)
    avatar = ProcessedImageField(upload_to='avatars',
                                 processors=[ResizeToFill(300, 300)],
                                 format='JPEG',
                                 default='avatars/no_avatar.jpg',
                                 options={'quality': 90})

    def image_tag(self):
        """Retorna url absoluta para uso html del avatar (imagen)"""
        return u'<img src="%s" alt= "404"/>' % self.avatar.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __string__(self):
        """Retorna el nombre de un usuario al imprimir un objeto Perfil"""
        return str(nombre)

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        perfil = Perfil(usuario=instance)
        perfil.save()
