# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0008_page_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=128)),
            ],
        ),
    ]
