# Generated by Django 3.2.16 on 2023-02-16 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0041_remove_collection_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='hide_collection_image',
            field=models.BooleanField(default=False),
        ),
    ]
