# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-19 12:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_image_cell'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='cell',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Cell'),
        ),
    ]
