from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from imagekit.processors import ResizeToFill
from django.forms.extras.widgets import SelectDateWidget


class Place(models.Model):
    placeName = models.CharField(max_length=50, null=True, blank=False)

    def __unicode__(self):
        return str(self.placeName)


class Photo(models.Model):
    picture = ProcessedImageField(upload_to='pictures',
                                  null=True,
                                  processors=[ResizeToFill(640, 480)],
                                  format='JPEG',
                                  options={'quality': 90})
    picture_crop = ImageSpecField(source='picture',
                                  processors=[ResizeToFill(50, 50)],
                                  format='JPEG',
                                  options={'quality': 60})
    date = models.DateField(null=True,
                            help_text="<em>yyyy-mm-dd</em>.")
    time = models.TimeField(null=True,
                            help_text="<em>hh:mm</em>.")
    place = models.ForeignKey(Place, null=True)

    def __unicode__(self):
        return str(self.dateTime)

    def image_tag(self):
        return u'<img src="%s" alt= "404"/>' % self.picture_crop.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
