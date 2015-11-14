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
    edad_privacidad = models.BooleanField("Privacidad", default=False)
    residencia = models.CharField(max_length=40, blank=True)
    residencia_privacidad = models.BooleanField("Privacidad", default=False)
    mail = models.EmailField(max_length=70, blank=True)
    mail_privacidad = models.BooleanField("Privacidad", default=False)
    facebook = models.URLField(max_length=60, blank=True)
    facebook_privacidad = models.BooleanField("Privacidad", default=False)
    web = models.URLField(max_length=200, blank=True)
    web_privacidad = models.BooleanField("Privacidad", default=False)
    avatar = ProcessedImageField(upload_to='avatars',
                                 processors=[ResizeToFill(300, 300)],
                                 format='JPEG',
                                 default='avatars/no_avatar.jpg',
                                 options={'quality': 90})
    # Lista de vinculos
    vinculos = models.ManyToManyField("self", through='Relationship',
                                      symmetrical=False,
                                      related_name='related_to+')

    def image_tag(self):
        """Retorna url absoluta para uso html del avatar (imagen)"""
        return u'<img src="%s" alt= "404"/>' % self.avatar.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __string__(self):
        """Retorna el nombre de un usuario al imprimir un objeto Perfil"""
        return str(self.nombre)

    def add_relationship(self, perfil, status, symm=True):
        relationship, created = Relationship.objects.get_or_create(
                                from_person=self,
                                to_person=perfil,
                                status=status)
        if symm:
            # avoid recursion by passing `symm=False`
            perfil.add_relationship(self, status, False)
        return relationship

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self)


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        perfil = Perfil(usuario=instance)
        perfil.save()


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)


class Relationship(models.Model):
    from_perfil = models.ForeignKey(Perfil, related_name='from_people')
    to_perfil = models.ForeignKey(Perfil, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
