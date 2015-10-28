# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoApp', '0003_photo_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'pictures'),
        ),
    ]
