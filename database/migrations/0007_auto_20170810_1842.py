# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 22:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20170810_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appsettings',
            name='show_hidden_notes',
        ),
        migrations.AddField(
            model_name='appsettings',
            name='exclude_hidden_notes',
            field=models.BooleanField(default=True),
        ),
    ]