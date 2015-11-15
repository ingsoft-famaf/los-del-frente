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

    def image_tag(self):
        """Retorna url absoluta para uso html del avatar (imagen)"""
        return u'<img src="%s" alt= "404"/>' % self.avatar.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __string__(self):
        """Retorna el nombre de un usuario al imprimir un objeto Perfil"""
        return str(self.nombre)


'''
 Tomada de aplicacion django-friends
'''


class FriendshipManager(models.Manager):

    # Lista de amistades para tal usuario
    def friends_for_user(self, user):
        friends = []
        for friendship in self.filter(from_user=user):
            friends.append({"friend": friendship.to_user, "friendship": friendship})
        for friendship in self.filter(to_user=user):
            friends.append({"friend": friendship.from_user, "friendship": friendship})
        return friends

    # 2 usuarios son amigos?
    def are_friends(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).count() > 0:
            return True
        if self.filter(from_user=user2, to_user=user1).count() > 0:
            return True
        return False


class Friendship(models.Model):
    """
    A friendship is a bi-directional association between two users who
    have both agreed to the association.
    """

    to_user = models.ForeignKey(User, related_name="friends")
    from_user = models.ForeignKey(User, related_name="_unused_")

    objects = FriendshipManager()

    class Meta:
        unique_together = (('to_user', 'from_user'),)

'''
 Lista de amistades para el usuario; accesible para una vista
'''


def friend_set_for(user):
    return set([obj["friend"] for obj in Friendship.objects.friends_for_user(user)])


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        perfil = Perfil(usuario=instance)
        perfil.save()
