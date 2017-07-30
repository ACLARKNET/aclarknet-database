# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 00:23
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0121_estimate_is_sow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsettings',
            name='dashboard_choices',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('data', 'Data'), ('invoices', 'Invoices'), ('notes', 'Notes'), ('projects', 'Projects'), ('times', 'Times'), ('totals', 'Totals')], max_length=41, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dashboard_choices',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('data', 'Data'), ('invoices', 'Invoices'), ('notes', 'Notes'), ('projects', 'Projects'), ('times', 'Times'), ('totals', 'Totals')], max_length=41, null=True),
        ),
    ]