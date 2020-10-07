# Generated by Django 2.1.5 on 2020-09-08 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0006_auto_20200908_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='matrix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matrix_cells', to='matrices.Matrix'),
        ),
    ]
