# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoApp', '0002_photo_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='place',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
