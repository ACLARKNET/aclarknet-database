# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-09 20:48
from __future__ import unicode_literals

from django.db import migrations
import relativedeltafield


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0091_project_flex_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='flex_date',
            field=relativedeltafield.RelativeDeltaField(blank=True, null=True),
        ),
    ]