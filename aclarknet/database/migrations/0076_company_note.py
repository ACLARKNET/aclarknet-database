# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-02 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0075_note_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='note',
            field=models.ManyToManyField(blank=True, to='database.Note'),
        ),
    ]
