# Generated by Django 4.2.4 on 2024-04-04 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0060_gateway'),
    ]

    operations = [
        migrations.AddField(
            model_name='environment',
            name='gateway',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='environments', to='matrices.gateway'),
        ),
        migrations.AddField(
            model_name='environment',
            name='gateway_pagination',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='environment',
            name='gateway_port',
            field=models.IntegerField(default=0),
        ),
    ]
