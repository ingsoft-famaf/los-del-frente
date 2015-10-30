# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoApp', '0006_auto_20151029_2054'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Example',
        ),
        migrations.AlterField(
            model_name='photo',
            name='picture',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=b'pictures'),
        ),
    ]
