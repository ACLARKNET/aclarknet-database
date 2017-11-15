# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-15 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0064_auto_20171115_0752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='dashboard_choices',
        ),
        migrations.AddField(
            model_name='newsletter',
            name='template_choices',
            field=models.CharField(blank=True, choices=[('html_mail.html', 'Mail'), ('cerberus-fluid.html', 'Fluid'), ('cerberus-hybrid.html', 'Hybrid'), ('cerberus-responsive.html', 'Responsive')], max_length=300, null=True, verbose_name='Template Choices'),
        ),
    ]
