# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ajaximage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoApp', '0005_auto_20151028_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thumbnail', ajaximage.fields.AjaxImageField()),
            ],
        ),
        migrations.AlterField(
            model_name='photo',
            name='picture',
            field=ajaximage.fields.AjaxImageField(null=True),
        ),
    ]
