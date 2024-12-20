# Generated by Django 5.1 on 2024-08-22 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environmentaldata',
            name='airQuality',
        ),
        migrations.RemoveField(
            model_name='environmentaldata',
            name='sunlight',
        ),
        migrations.RemoveField(
            model_name='soildata',
            name='exchangeableAcid',
        ),
        migrations.AddField(
            model_name='soildata',
            name='soilTemperature',
            field=models.DecimalField(decimal_places=2, help_text='Temperature of the soil', max_digits=5, null=True, verbose_name='Soil Temperature'),
        ),
    ]
