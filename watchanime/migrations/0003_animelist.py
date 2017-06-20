# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchanime', '0002_auto_20160531_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimeList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animeName', models.CharField(max_length=140)),
                ('releaseDay', models.IntegerField()),
                ('releaseTime', models.TimeField()),
                ('currentEpisode', models.IntegerField()),
                ('maxEpisodes', models.IntegerField()),
            ],
        ),
    ]
