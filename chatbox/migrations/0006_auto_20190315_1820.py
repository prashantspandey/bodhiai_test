# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-03-15 12:50
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbox', '0005_contextdetail_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='chathistory',
            name='nextPosition',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=['None'], size=None),
        ),
        migrations.AddField(
            model_name='chathistory',
            name='repeat',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(default=False), default=[False], size=None),
        ),
    ]
