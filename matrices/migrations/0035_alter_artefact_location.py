# Generated by Django 3.2.15 on 2022-10-04 09:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0034_auto_20220901_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artefact',
            name='location',
            field=models.FileField(max_length=500, upload_to='', validators=[django.core.validators.FileExtensionValidator(['zip'])]),
        ),
    ]
