# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-13 15:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0050_auto_20170613_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='statement_of_work',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Estimate'),
        ),
    ]
