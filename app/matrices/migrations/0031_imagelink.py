# Generated by Django 3.2.15 on 2022-08-26 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0030_auto_20220801_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artefact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='file', to='matrices.document')),
                ('child_image', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='child', to='matrices.image')),
                ('parent_image', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent', to='matrices.image')),
            ],
        ),
    ]
