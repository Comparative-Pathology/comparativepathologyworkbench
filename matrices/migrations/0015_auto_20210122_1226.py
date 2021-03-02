# Generated by Django 3.1.2 on 2021-01-22 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrices', '0014_auto_20200929_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionAuthority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=12, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='collectionauthorities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionAuthorisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collectionauthorisations', to='matrices.matrix')),
                ('collection_authority', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='collectionauthorisations', to='matrices.collectionauthority')),
                ('permitted', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='collectionauthorisations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='', max_length=4095)),
                ('images', models.ManyToManyField(related_name='collectionimage', to='matrices.Image')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='collections', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='matrix',
            name='last_used_collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='collections', to='matrices.collection'),
        ),
    ]