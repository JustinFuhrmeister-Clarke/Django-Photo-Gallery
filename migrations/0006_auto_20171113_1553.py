# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0005_auto_20171112_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='preview_file',
            field=models.ImageField(null=True, upload_to='photo_files/previews'),
        ),
        migrations.AddField(
            model_name='photo',
            name='thumbnail_file',
            field=models.ImageField(null=True, upload_to='photo_files/thumbnails'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image_file',
            field=models.ImageField(upload_to='photo_files/upload'),
        ),
    ]
