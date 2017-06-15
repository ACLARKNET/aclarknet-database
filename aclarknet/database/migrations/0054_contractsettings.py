# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0053_contract_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parties', models.TextField(blank=True, null=True)),
                ('scope_of_work', models.TextField(blank=True, null=True)),
                ('payment_terms', models.TextField(blank=True, null=True)),
                ('timing_of_payment', models.TextField(blank=True, null=True)),
                ('contributor_assignment_agreement', models.TextField(blank=True, null=True)),
                ('authority_to_act', models.TextField(blank=True, null=True)),
                ('termination', models.TextField(blank=True, null=True)),
                ('governing_laws', models.TextField(blank=True, null=True)),
                ('period_of_agreement', models.TextField(blank=True, null=True)),
                ('confidentiality', models.TextField(blank=True, null=True)),
                ('taxes', models.TextField(blank=True, null=True)),
                ('limited_warranty', models.TextField(blank=True, null=True)),
                ('complete_agreement', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
