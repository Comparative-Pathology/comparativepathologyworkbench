# Generated by Django 3.1.2 on 2021-02-17 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0021_remove_image_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='image', to='matrices.image'),
        ),
    ]
