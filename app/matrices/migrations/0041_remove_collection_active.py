# Generated by Django 3.2.15 on 2022-11-24 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0040_auto_20221122_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='active',
        ),
    ]