# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-25 19:59
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0065_profile_dashboard_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dashboard_choices',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('data', 'Data'), ('invoices', 'Invoices'), ('notes', 'Notes'), ('projects', 'Projects'), ('totals', 'Totals')], max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='dashboard_choices',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('data', 'Data'), ('invoices', 'Invoices'), ('notes', 'Notes'), ('projects', 'Projects'), ('totals', 'Totals')], max_length=35, null=True),
        ),
    ]
