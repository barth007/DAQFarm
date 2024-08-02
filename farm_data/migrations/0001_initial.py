# Generated by Django 5.0.7 on 2024-08-02 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_name', models.CharField(help_text='Name of the element', max_length=50, unique=True, verbose_name='Element Name')),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Last updated date', verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last updated date', verbose_name='Last Updated Date')),
                ('status', models.CharField(default='active', help_text='is the  object active', max_length=20, verbose_name='is_active')),
                ('name', models.CharField(help_text='The name of the plot', max_length=50, unique=True, verbose_name='Plot Name')),
                ('current_crop_type', models.CharField(help_text='Current crop cultivated', max_length=250, verbose_name='Current Crop Type')),
                ('plot_status', models.CharField(choices=[('normal', 'Normal'), ('warning', 'Warning'), ('good', 'Good')], default='normal', help_text='Current status of the plot', max_length=50, verbose_name='status')),
                ('last_sync_time', models.DateTimeField(auto_now=True, help_text='Last time the plot data was synchronized', verbose_name='Last Sync Time')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnvironmentalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Last updated date', verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last updated date', verbose_name='Last Updated Date')),
                ('status', models.CharField(default='active', help_text='is the  object active', max_length=20, verbose_name='is_active')),
                ('temperature', models.DecimalField(decimal_places=2, help_text='Environment temperature', max_digits=5, verbose_name='Temperature')),
                ('humidity', models.DecimalField(decimal_places=2, help_text='Environment humdity percentage', max_digits=5, verbose_name='Humidity')),
                ('pressure', models.DecimalField(decimal_places=2, help_text='Atmospheric pressure', max_digits=5, verbose_name='Pressure')),
                ('natural_gas', models.DecimalField(decimal_places=2, help_text='Natural gas concentration', max_digits=5, verbose_name='Natural Gas')),
                ('sunlight', models.DecimalField(decimal_places=2, help_text='Sunlight intensity', max_digits=5, verbose_name='Sunlight')),
                ('air_quality', models.DecimalField(decimal_places=2, help_text='Air quality of the enviroment', max_digits=5, verbose_name='Air Quality')),
                ('plot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_data.plot')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ElementData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Last updated date', verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last updated date', verbose_name='Last Updated Date')),
                ('status', models.CharField(default='active', help_text='is the  object active', max_length=20, verbose_name='is_active')),
                ('element_value', models.DecimalField(blank=True, decimal_places=2, help_text='Value of the element', max_digits=5, null=True, verbose_name='Element Value')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_data.element')),
                ('plot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_data.plot')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlotHardWareData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Last updated date', verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last updated date', verbose_name='Last Updated Date')),
                ('status', models.CharField(default='active', help_text='is the  object active', max_length=20, verbose_name='is_active')),
                ('battery_status', models.DecimalField(decimal_places=2, help_text='Temperature of the board', max_digits=4, verbose_name='Board Temperature')),
                ('solar_panel_voltage', models.DecimalField(decimal_places=2, help_text='Voltage of the solar panel', max_digits=4, verbose_name='Solar panel voltage')),
                ('board_temperature', models.DecimalField(decimal_places=1, help_text='Battery status percentage', max_digits=4, verbose_name='Battery status')),
                ('plot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_data.plot')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SoilData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Last updated date', verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last updated date', verbose_name='Last Updated Date')),
                ('status', models.CharField(default='active', help_text='is the  object active', max_length=20, verbose_name='is_active')),
                ('moisture', models.DecimalField(decimal_places=2, help_text='Soil moisture percentage', max_digits=5, verbose_name='Soil Moisture')),
                ('ph_level', models.DecimalField(decimal_places=2, help_text='PH level of the soil', max_digits=5, verbose_name='PH Level')),
                ('electrical_conductivity', models.DecimalField(decimal_places=2, help_text='Electrical conductivity of the soil', max_digits=5, verbose_name='Electrical Conductivity')),
                ('exchangeable_acid', models.DecimalField(decimal_places=2, help_text='Exchangeable acidity in the soil', max_digits=5, verbose_name='Exchangeable Acidity')),
                ('plot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_data.plot')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
