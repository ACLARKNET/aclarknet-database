# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 22:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0048_settingscontract'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settingsapp',
            old_name='auto_hide_notes',
            new_name='auto_hide',
        ),
    ]
