# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 14:05
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventary', '0002_auth_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='view_limit',
            field=models.IntegerField(help_text='limits the number of daily anonymous views for proposed events', verbose_name='view limit'),
        ),
        migrations.AlterField(
            model_name='event',
            name='calendar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventary.Calendar', verbose_name='calendar'),
        ),
        migrations.AlterField(
            model_name='event',
            name='comment',
            field=models.CharField(blank=True, help_text='comment', max_length=255, null=True, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, help_text='description', null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='cal/documents/%Y/%m/%d', verbose_name='document'),
        ),
        migrations.AlterField(
            model_name='event',
            name='homepage',
            field=models.URLField(blank=True, null=True, verbose_name='homepage'),
        ),
        migrations.AlterField(
            model_name='event',
            name='host',
            field=models.CharField(max_length=255, verbose_name='host'),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cal/images/%Y/%m/%d', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='event',
            name='prize',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='prize', max_digits=6, null=True, verbose_name='prize'),
        ),
        migrations.AlterField(
            model_name='event',
            name='published',
            field=models.BooleanField(help_text='publication status', verbose_name='published'),
        ),
        migrations.AlterField(
            model_name='event',
            name='recurring',
            field=models.BooleanField(default=False, help_text='recurring event', verbose_name='recurring event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='eventtimedate',
            name='comment',
            field=models.CharField(blank=True, help_text='comment', max_length=255, null=True, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='eventtimedate',
            name='end_date',
            field=models.DateField(blank=True, help_text='end date', null=True, verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='eventtimedate',
            name='end_time',
            field=models.TimeField(blank=True, help_text='end time', null=True, verbose_name='end time'),
        ),
        migrations.AlterField(
            model_name='eventtimedate',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventary.Event', verbose_name='event'),
        ),
        migrations.AlterField(
            model_name='eventtimedate',
            name='start_date',
            field=models.DateField(help_text='start date', verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='eventtimedate',
            name='start_time',
            field=models.TimeField(blank=True, help_text='start time', null=True, verbose_name='start time'),
        ),
        migrations.AlterField(
            model_name='group',
            name='events',
            field=models.ManyToManyField(blank=True, to='eventary.Event', verbose_name='events'),
        ),
        migrations.AlterField(
            model_name='group',
            name='grouping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventary.Grouping', verbose_name='grouping'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='grouping',
            name='calendars',
            field=models.ManyToManyField(blank=True, to='eventary.Calendar', verbose_name='calendar'),
        ),
        migrations.AlterField(
            model_name='grouping',
            name='grouping_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventary.GroupingType', verbose_name='grouping type'),
        ),
        migrations.AlterField(
            model_name='grouping',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='groupingtype',
            name='label',
            field=models.CharField(max_length=255, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='host',
            name='homepage',
            field=models.URLField(verbose_name='homepage'),
        ),
        migrations.AlterField(
            model_name='host',
            name='organization',
            field=models.CharField(help_text='hosting organization', max_length=49, verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='host',
            name='phone',
            field=models.CharField(max_length=19, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='secret',
            name='calls',
            field=models.IntegerField(default=0, verbose_name='calls'),
        ),
        migrations.AlterField(
            model_name='secret',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='secret',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='eventary.Event', verbose_name='event'),
        ),
        migrations.AlterField(
            model_name='secret',
            name='last_call',
            field=models.DateField(null=True, verbose_name='last call'),
        ),
        migrations.AlterField(
            model_name='secret',
            name='secret',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='secret'),
        ),
    ]
