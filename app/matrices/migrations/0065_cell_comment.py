# Generated by Django 4.2.4 on 2024-09-25 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0064_rename_order_collectionimageorder_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
