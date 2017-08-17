# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_profile_icon_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsettings',
            name='icon_color',
            field=models.CharField(blank=True, choices=[('danger', 'Danger'), ('faded', 'Faded'), ('info', 'Info'), ('inverse', 'Inverse'), ('primary', 'Primary'), ('success', 'Success'), ('warning', 'Warning')], max_length=255, null=True),
        ),
    ]
