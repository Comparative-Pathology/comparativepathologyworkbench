# Generated by Django 3.2.15 on 2022-10-14 09:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0037_alter_document_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artefact',
            name='location',
            field=models.FileField(blank=True, max_length=500, upload_to='', validators=[django.core.validators.FileExtensionValidator(['zip'])]),
        ),
    ]
