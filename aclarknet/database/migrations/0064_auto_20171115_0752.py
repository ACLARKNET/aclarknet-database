# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-15 12:52
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0063_auto_20171107_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='dashboard_choices',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('html_mail.html', 'Mail'), ('cerberus-fluid.html', 'Fluid'), ('cerberus-hybrid.html', 'Hybrid'), ('cerberus-responsive.html', 'Responsive')], max_length=80, null=True, verbose_name='Template Choices'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dashboard_choices',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('estimates', 'Estimates'), ('invoices', 'Invoices'), ('notes', 'Notes'), ('plot', 'Plot'), ('projects', 'Projects'), ('times', 'Times'), ('totals', 'Totals')], max_length=51, null=True, verbose_name='Dashboard Choices'),
        ),
    ]
