# Generated by Django 3.2.15 on 2022-11-22 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrices', '0038_alter_artefact_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='active_collections', to='matrices.collection')),
                ('last_used_collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lastused_collections', to='matrices.collection')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preference', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
