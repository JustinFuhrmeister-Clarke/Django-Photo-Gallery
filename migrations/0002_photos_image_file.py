# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photos',
            name='image_file',
            field=models.ImageField(default=12, upload_to=''),
            preserve_default=False,
        ),
    ]