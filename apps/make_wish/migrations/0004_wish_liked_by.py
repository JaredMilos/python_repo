# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make_wish', '0003_auto_20180924_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='liked_by',
            field=models.ManyToManyField(related_name='likes', to='make_wish.User'),
        ),
    ]
