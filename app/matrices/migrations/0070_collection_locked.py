# Generated by Django 4.2.4 on 2024-11-26 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0069_remove_environment_broker_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='locked',
            field=models.BooleanField(default=False),
        ),
    ]
