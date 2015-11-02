# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('edad', models.IntegerField()),
                ('residencia', models.CharField(max_length=40)),
                ('mail', models.EmailField(max_length=70)),
                ('facebook', models.URLField(max_length=60)),
                ('web', models.URLField()),
                ('es_moderador', models.BooleanField()),
            ],
        ),
    ]
