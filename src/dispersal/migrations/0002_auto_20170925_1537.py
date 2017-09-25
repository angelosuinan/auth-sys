# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-25 07:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20170822_2231'),
        ('dispersal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('date_acquired', models.DateField()),
                ('customer_name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=2)),
                ('address', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=11)),
                ('region', models.CharField(max_length=20)),
                ('remarks', models.TextField(blank=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='employee.EmployeeProfile')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='dispersal.Payment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='order',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='order',
            name='fish',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
