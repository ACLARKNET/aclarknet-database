# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
