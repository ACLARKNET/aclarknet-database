# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 21:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0116_worldborder'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WorldBorder',
            new_name='World',
        ),
    ]
