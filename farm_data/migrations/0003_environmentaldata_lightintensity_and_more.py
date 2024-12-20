# Generated by Django 5.1 on 2024-08-28 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_data', '0002_remove_environmentaldata_airquality_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='environmentaldata',
            name='lightIntensity',
            field=models.DecimalField(decimal_places=2, help_text='Sunlight intensity', max_digits=5, null=True, verbose_name='Sunlight Intensity'),
        ),
        migrations.AddField(
            model_name='plothardwaredata',
            name='localTime',
            field=models.DateTimeField(help_text='Local time of the device', null=True, verbose_name='Local Time'),
        ),
        migrations.AddField(
            model_name='plothardwaredata',
            name='orientation',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Orientation of the device', max_digits=4, null=True, verbose_name='Orientation'),
        ),
    ]
