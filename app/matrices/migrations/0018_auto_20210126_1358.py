# Generated by Django 3.1.2 on 2021-01-26 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0017_auto_20210125_1124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authorisation',
            options={'verbose_name': 'Authorisation', 'verbose_name_plural': 'Authorisations'},
        ),
        migrations.AlterModelOptions(
            name='matrix',
            options={'verbose_name': 'Bench', 'verbose_name_plural': 'Benches'},
        ),
        migrations.AlterField(
            model_name='collectionauthorisation',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collectionauthorisations', to='matrices.collection'),
        ),
    ]
