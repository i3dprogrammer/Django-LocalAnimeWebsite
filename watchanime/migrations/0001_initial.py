# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-31 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('episode', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('path', models.TextField()),
            ],
        ),
    ]