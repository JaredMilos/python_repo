# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make_wish', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='granted_flag',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
