# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoApp', '0007_auto_20151029_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placeName', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='photo',
            name='place',
            field=models.ForeignKey(to='PhotoApp.Place', null=True),
        ),
    ]
