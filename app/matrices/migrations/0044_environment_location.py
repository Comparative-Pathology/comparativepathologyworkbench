# Generated by Django 3.2.16 on 2023-02-28 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0043_environment_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='environment',
            name='location',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='environments', to='matrices.location'),
        ),
    ]