from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator
from PhotoApp.models import Notification
from PhotoApp.models import Place


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
    avatar_crop = ImageSpecField(source='avatar',
                                 processors=[ResizeToFill(80, 80)],
                                 format='JPEG',
                                 options={'quality': 90})

    def image_tag(self):
        """Retorna url absoluta para uso html del avatar (imagen)"""
        return u'<img src="%s" alt= "404"/>' % self.avatar_crop.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __string__(self):
        """Retorna el nombre de un usuario al imprimir un objeto Perfil"""
        return str(self.nombre)


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    '''
    Metodo que crea automaticamente un perfil (minimal) para un usuario nuevo
    recientemente registrado
    '''
    if created:
        perfil = Perfil(usuario=instance)
        perfil.save()
        welcome = Notification(text="Bienvenido a Photolink :)",
                               receiver=instance)
        welcome.save()


class FriendshipManager(models.Manager):
    '''
     Tomada de aplicacion django-friends
    '''
    # Lista de amistades para tal usuario
    def friends_for_user(self, user):
        friends = []
        for friendship in self.filter(from_user=user):
            friends.append({"friend": friendship.to_user,
                            "friendship": friendship})
        for friendship in self.filter(to_user=user):
            friends.append({"friend": friendship.from_user,
                            "friendship": friendship})
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


def friend_set_for(user):
    '''
    Metodo que retorna el grupo de amigos para un determinado usuario.
    '''
    return set([obj["friend"] for obj in
               Friendship.objects.friends_for_user(user)])


INVITE_STATUS = (
    ("0", "Unanswered"),
    ("1", "Accepted"),
    ("2", "Declined"),
)


class FriendshipInvitationManager(models.Manager):

    def invitations(self, *args, **kwargs):
        return self.filter(*args, **kwargs).exclude(
                           status__in=["2"]).exclude(status__in=["1"])



class FriendshipInvitation(models.Model):
    """
    A frienship invite is an invitation from one user to another to be
    associated as friends.
    """

    from_user = models.ForeignKey(User, related_name="invitations_from")
    to_user = models.ForeignKey(User, related_name="invitations_to")
    status = models.CharField(max_length=1, choices=INVITE_STATUS)

    objects = FriendshipInvitationManager()

    def accept(self):
        if not Friendship.objects.are_friends(self.to_user, self.from_user):
            friendship = Friendship(to_user=self.to_user, from_user=self.from_user)
            friendship.save()
            self.status = "1"
            self.save()

    def decline(self):
        if not Friendship.objects.are_friends(self.to_user, self.from_user):
            self.status = "2"
            self.save()

"""
Me devuelve todos aquellos que tienen solicitudes pendientes que involucran
a user.
Motivacion: que no se le pueda mandar una solicitud a ellos
"""
def wanna_be_friends(user):

    my_invitations = FriendshipInvitation.objects.invitations()
    future_friends=[]
    for invitation in my_invitations:
        if invitation.to_user==user and invitation.\
                from_user not in future_friends:
            future_friends.append(invitation.from_user)
        if invitation.from_user==user and invitation.\
                to_user not in future_friends:
            future_friends.append(invitation.to_user)
    return future_friends
