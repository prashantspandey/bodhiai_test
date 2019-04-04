# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-02-19 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0006_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
