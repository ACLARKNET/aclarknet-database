# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0125_time_cog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsettings',
            name='dashboard_choices',
            field=models.CharField(blank=True, choices=[('data', 'Data'), ('invoices', 'Invoices'), ('notes', 'Notes'), ('projects', 'Projects'), ('times', 'Times'), ('totals', 'Totals')], max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dashboard_choices',
            field=models.CharField(blank=True, choices=[('data', 'Data'), ('invoices', 'Invoices'), ('notes', 'Notes'), ('projects', 'Projects'), ('times', 'Times'), ('totals', 'Totals')], max_length=1000, null=True),
        ),
    ]
