# Generated by Django 3.2.13 on 2022-06-28 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0027_auto_20220628_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='description',
            field=models.TextField(blank=True, default='', max_length=4095),
        ),
        migrations.AlterField(
            model_name='cell',
            name='title',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]