# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-19 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20181119_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='cell',
        ),
    ]
