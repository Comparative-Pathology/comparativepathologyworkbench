# Generated by Django 3.1 on 2020-08-26 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0002_auto_20200826_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorisation',
            name='matrix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matrixauthorisations', to='matrices.matrix'),
        ),
    ]
