# Generated by Django 2.1.5 on 2020-09-09 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0008_auto_20200909_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='image_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
