# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 10:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0049_auto_20170903_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settingsapp',
            name='created',
        ),
        migrations.RemoveField(
            model_name='settingsapp',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='settingscompany',
            name='created',
        ),
        migrations.RemoveField(
            model_name='settingscompany',
            name='updated',
        ),
    ]