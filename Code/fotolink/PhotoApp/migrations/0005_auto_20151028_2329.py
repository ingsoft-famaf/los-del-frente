# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoApp', '0004_auto_20151028_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='picture',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=b'pictures'),
        ),
    ]
