from django.db import models

# Create your models here.

class Photo(models.Model):
    picture = models.ImageField(upload_to='pictures', null = True)
    dateTime = models.DateTimeField(null= True)
    place = models.CharField(max_length=50, null=True)

    # This is how an object is shown
    def __unicode__(self):
        return str(self.place) + ' ' + str (self.dateTime)

    # This is only for thumbnail of the picture in admin
    def image_tag(self):
        return u'<img src="%s" alt= "404"/>' % self.picture.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
