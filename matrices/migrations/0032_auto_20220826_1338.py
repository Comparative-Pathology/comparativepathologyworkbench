# Generated by Django 3.2.15 on 2022-08-26 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrices', '0031_imagelink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artefact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='', max_length=4095)),
                ('location', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='artefacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='imagelink',
            name='artefact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='file', to='matrices.artefact'),
        ),
    ]
