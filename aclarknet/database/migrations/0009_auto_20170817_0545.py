# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20170813_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsettings',
            name='icon_size',
            field=models.CharField(blank=True, choices=[('1x', 'Small'), ('2x', 'Medium'), ('3x', 'Large'), ('4x', 'XL'), ('5x', 'XXL')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='icon_size',
            field=models.CharField(blank=True, choices=[('1x', 'Small'), ('2x', 'Medium'), ('3x', 'Large'), ('4x', 'XL'), ('5x', 'XXL')], max_length=255, null=True),
        ),
    ]