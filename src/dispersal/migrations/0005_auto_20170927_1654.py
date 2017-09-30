# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-27 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispersal', '0004_payment_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Organization')], default='M', max_length=2)),
                ('telephone', models.CharField(max_length=11)),
                ('region', models.CharField(choices=[('I', 'REGION I (Ilocos Region) in Luzon'), ('II', 'REGION 2 (Cagayan Valley) in Luzon'), ('III', 'REGION III (Central Luzon)'), ('IV-A', 'REGION IV-A (CALABARZON) Luzon'), ('IV-B', 'REGION IV-B(MIMAROPA) 17th region Visayas'), ('V', 'REGION V(Bicol Region) Luzon'), ('VI', 'REGION VI (Western Visayas'), ('VII', 'REGION VII (Central Visayas'), ('VIII', 'REGION VIII (Eastern Visayas)'), ('IX', 'REGION IX (Zamboanga Peninsula)'), ('X', 'REGION X (Northern Mindanao)'), ('XI', 'REGION XI (Davao Region)'), ('XII', 'REGION XII (Soccsksargen)'), ('XIII', 'REGION XIII (CARAGA)'), ('NCR', '(NCR) National Capital Region in Luzon'), ('XIV', 'REGION 14 Cordillera Administrative Region (CAR) in Luzon'), ('XV', 'REGION XV - Autonomous Region in Muslim Mindanao (ARMM)'), ('XVIII', 'Region XVIII - NIR - Negros Island Region')], default='NCR', max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='address',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='region',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='telephone',
        ),
    ]