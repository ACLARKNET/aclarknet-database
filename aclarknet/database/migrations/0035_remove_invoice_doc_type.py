# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 13:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0034_invoice_doc_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='doc_type',
        ),
    ]