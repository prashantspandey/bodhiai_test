# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-02-15 06:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0004_awskey'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentChallenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('studentOne', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studentone', to='basicinformation.Student')),
                ('studentTwo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studenttwo', to='basicinformation.Student')),
            ],
        ),
    ]
