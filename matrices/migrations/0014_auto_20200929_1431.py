# Generated by Django 2.1.5 on 2020-09-29 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0013_auto_20200928_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='url',
            new_name='url_blog',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='url',
            new_name='url_server',
        ),
    ]
