# Generated by Django 3.2.13 on 2022-08-01 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0029_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='comment',
            field=models.TextField(default='', max_length=4095),
        ),
        migrations.AlterField(
            model_name='document',
            name='location',
            field=models.FileField(upload_to=''),
        ),
    ]