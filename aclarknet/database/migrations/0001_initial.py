# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 01:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('address', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('estimate_counter', models.IntegerField(blank=True, null=True, verbose_name=b'Estimate Counter')),
                ('invoice_counter', models.IntegerField(blank=True, null=True, verbose_name=b'Invoice Counter')),
                ('currency_symbol', models.CharField(blank=True, default=b'$', max_length=300, null=True, verbose_name=b'Currency Symbol')),
            ],
            options={
                'verbose_name': 'Company',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=300, null=True)),
                ('last_name', models.CharField(blank=True, max_length=300, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('office_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name=b'Issue Date')),
                ('subject', models.CharField(blank=True, max_length=300, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name=b'Estimate Amount')),
                ('document_id', models.IntegerField(blank=True, null=True, verbose_name=b'Estimate ID')),
                ('discount', models.IntegerField(blank=True, null=True)),
                ('tax', models.IntegerField(blank=True, null=True)),
                ('tax2', models.IntegerField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, default=b'United States Dollar - USD', max_length=300, null=True)),
                ('accepted_date', models.DateField(blank=True, null=True)),
                ('declined_date', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name=b'Issue Date')),
                ('last_payment_date', models.DateField(blank=True, null=True)),
                ('document_id', models.IntegerField(blank=True, null=True, verbose_name=b'Invoice ID')),
                ('po_number', models.CharField(blank=True, max_length=300, null=True, verbose_name=b'PO Number')),
                ('subject', models.CharField(blank=True, max_length=300, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name=b'Invoice Amount')),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('discount', models.IntegerField(blank=True, null=True)),
                ('tax', models.IntegerField(blank=True, null=True)),
                ('tax2', models.IntegerField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, default=b'United States Dollar - USD', max_length=300, null=True)),
                ('currency_symbol', models.CharField(blank=True, default=b'$', max_length=300, null=True)),
                ('document_type', models.CharField(blank=True, max_length=300, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('unit', models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=12, null=True, verbose_name=b'Unit')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=300, null=True, unique=True, verbose_name=b'Project Name')),
                ('code', models.IntegerField(blank=True, null=True, verbose_name=b'Project Code')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('total_hours', models.FloatField(blank=True, null=True)),
                ('billable_hours', models.FloatField(blank=True, null=True)),
                ('billable_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('budget_spent', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('budget_remaining', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('total_costs', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('team_costs', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('expenses', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('billable', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('unit', models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=12, null=True, verbose_name=b'Unit')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('project_code', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('hours', models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=12, null=True, verbose_name=b'Hours')),
                ('billable', models.BooleanField(default=True)),
                ('invoiced', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=300, null=True)),
                ('last_name', models.CharField(blank=True, max_length=300, null=True)),
                ('department', models.CharField(blank=True, max_length=300, null=True)),
                ('employee', models.BooleanField(default=True)),
                ('cost_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cost_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('currency', models.CharField(blank=True, max_length=300, null=True)),
                ('external_reference_url', models.URLField(blank=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Client')),
                ('estimate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Estimate')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Invoice')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Project')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Task')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Task'),
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invoice',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Project'),
        ),
    ]
