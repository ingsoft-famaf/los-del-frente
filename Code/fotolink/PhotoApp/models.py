from django.db import models

# Create your models here.

class Photo(models.Model):
    picture = models.ImageField(upload_to='pictures', null = True)
    dateTime = models.DateTimeField(null= True)
    place = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return str(self.place) + ' ' + str(self.dateTime)
