from django.db import models

# Create your models here.

class Photo(models.Model):
    picture = models.ImageField(upload_to='pictures', null = True, blank = True)
