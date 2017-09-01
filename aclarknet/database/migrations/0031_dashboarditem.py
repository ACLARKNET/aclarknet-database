# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0030_auto_20170830_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
    ]
