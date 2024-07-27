#farm_data/models.py
from django.db import models
from typing import Dict, List
from common.models import BaseModel
from datetime import datetime, timedelta
from django.utils.timesince import timesince
from django.core.exceptions import ValidationError

HELP_TEXT_AND_VERBOSE_NAME: Dict[str, Dict[str, List[str]]] = {
    'plot':{
        'name':['The name of the plot', 'Plot Name'],
        'plot_status': ['Current status of the plot', 'status'],
        'current_crop_type':['Current crop cultivated', 'Current Crop Type'],
        'last_sync_time': ['Last time the plot data was synchronized', 'Last Sync Time'],
    },
    'plot_hardware':{
        'solar_panel_voltage':['Voltage of the solar panel', 'Solar panel voltage'],
        'board_temperature': ['Temperature of the board', 'Board Temperature'],
        'battery_status':['Battery status percentage', 'Battery status'],
    },
    'soil':{
        'moisture':['Soil moisture percentage', 'Soil Moisture'],
        'ph_level': ['PH level of the soil', 'PH Level'],
        'electrical_conductivity': ['Electrical conductivity of the soil', 'Electrical Conductivity'],
        'exchangeable_acid':['Exchangeable acidity in the soil', 'Exchangeable Acidity'],
    },
    'environment': {
        'temperature': ['Environment temperature', 'Temperature'],
        'humidity': ['Environment humdity percentage', 'Humidity'],
        'pressure': ['Atmospheric pressure', 'Pressure'],
        'natural_gas': ['Natural gas concentration', 'Natural Gas'],
        'sunlight': ['Sunlight intensity', 'Sunlight'],
        'air_quality':['Air quality of the enviroment', 'Air Quality']
    },
    'element': {
        'element_name': ['Name of the element', 'Element Name'],
        'element_value': ['Value of the element', 'Element Value'],
    },

}



class Plot(BaseModel):
    (
        name_,
        plot_status_,
        current_crop_type_,
        last_sync_time_,
    )= HELP_TEXT_AND_VERBOSE_NAME["plot"].values()

    PLOT_STATUS =(
        ('normal', 'Normal'),
        ('warning', 'Warning'),
        ('good', 'Good'),
    )

    name = models.CharField(
        max_length=50,
        verbose_name=name_[1],
        help_text=name_[0],
        unique=True,
    )
    current_crop_type = models.CharField(
        max_length=250,
        verbose_name=current_crop_type_[1],
        help_text=current_crop_type_[0],
        unique=True,
    )
    plot_status = models.CharField(
        max_length=50,
        choices=PLOT_STATUS,
        default='normal',
        verbose_name=plot_status_[1],
        help_text=plot_status_[0],
    )
    
    last_sync_time=models.DateTimeField(
        auto_now=True,
        verbose_name=last_sync_time_[1],
        help_text=last_sync_time_[0],
    )

   
    def clean(self)-> None:
        super.clean()
        if Plot.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError({'name': 'A plot with this name already exists.'})


    @property
    def last_sync_time_calculated(self) -> str:
        return timesince(self.last_sync_time)
    

    def __str__(self)->str:
        return self.name
    

class PlotHardWareData(BaseModel):
    (
        solar_panel_voltage_,
        battery_status_,
        board_temperature_,
    )= HELP_TEXT_AND_VERBOSE_NAME['plot_hardware'].values()

    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    battery_status = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=battery_status_[1],
        help_text=battery_status_[0],
    )
    solar_panel_voltage = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=solar_panel_voltage_[1],
        help_text=solar_panel_voltage_[0]
    )
    board_temperature = models.DecimalField(
        max_digits=4, 
        decimal_places=1,
        verbose_name=board_temperature_[1],
        help_text=board_temperature_[0]
    )
    
    def clean(self) -> None:
        super().clean()
        if self.battery_status < 0 or self.battery_status > 100:
            raise ValidationError({'battery_status': 'Battery status must be between 0 and 100.'})
        if self.solar_panel_voltage < 0:
            raise ValidationError({'solar_panel_voltage': 'Solar panel voltage cannot be negative.'})
        if self.board_temperature < -50 or self.board_temperature > 150:
            raise ValidationError({'board_temperature': 'Board temperature must be between -50 and 150 degrees Celsius.'})
    
    def __str__(self) -> str:

        return self.plot.name
    
class SoilData(BaseModel):
    (
        moisture_,
        ph_level_,
        electrical_conductivity_,
        exchangeable_acid_,
    )=HELP_TEXT_AND_VERBOSE_NAME["soil"].values()

    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)

    moisture = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=moisture_[1],
        help_text=moisture_[0]
    )
    ph_level = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=ph_level_[1],
        help_text=ph_level_[0]
    )
    electrical_conductivity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=electrical_conductivity_[1],
        help_text=electrical_conductivity_[0]
    )
    exchangeable_acid = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=exchangeable_acid_[1],
        help_text=exchangeable_acid_[0]
    )

    def clean(self):
        super.clean()
        if self.moisture < 0 or self.moisture > 100:
            raise ValidationError({'moisture': 'Moisture must be between 0 and 100.'})
        if self.ph_level < 0 or self.ph_level > 14:
            raise ValidationError({'ph_level': 'pH level must be between 0 and 14.'})
        if  self.electrical_conductivity < 0 :
            raise ValidationError({'electrical_conductivity': 'Electrical conductivity cannot be negative.'})
        if self.exchangeable_acid < 0:
            raise ValidationError({'exhangeable_acid':'Exchangeable acidity cannot be negative'})

    def __str__(self)->str:
        return f"soil data for {self.plot.name}"
    

class EnvironmentalData(BaseModel):
    (
        temperature_,
        humidity_,
        pressure_,
        natural_gas_,
        sunlight_,
        air_quality_,
    )=HELP_TEXT_AND_VERBOSE_NAME['environment'].values()

    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)

    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=temperature_[1],
        help_text=temperature_[0]
    )
    humidity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=humidity_[1],
        help_text=humidity_[0]
    )
    pressure = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=pressure_[1],
        help_text=pressure_[0]
    )
    natural_gas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=natural_gas_[1],
        help_text=natural_gas_[0]
    )
    sunlight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=sunlight_[1],
        help_text=sunlight_[0]
    )
    air_quality = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=air_quality_[1],
        help_text=air_quality_[0]
    )

    def clean (self):
        super.clean()
        if self.temperature < -50 or self.temperature > 60:
            raise ValidationError({'temperature': 'Temperature must be between -50 and 60 degrees Celsius.'})
        if self.humidity < 0 or self.humidity > 100:
            raise ValidationError({'humidity': 'Humidity must be between 0 and 100%.'})
        if self.pressure < 300 or self.pressure > 1100:
            raise ValidationError({'pressure': 'Pressure must be between 300 and 1100 hPa.'})
        if self.natural_gas < 0:
            raise ValidationError({'natural_gas': 'Natural gas concentration cannot be negative.'})
        if self.sunlight < 0:
            raise ValidationError({'sunlight': 'Sunlight intensity cannot be negative.'})
        if self.air_quality < 0 or self.air_quality > 500:
            raise ValidationError({'air_quality': 'Air quality index must be between 0 and 500.'})

    def __str__(self)-> str:
        return f"Environment data for {self.plot.name}"


class Element(models.Model):
    (
        element_name_,
        element_value_,
    ) = HELP_TEXT_AND_VERBOSE_NAME['element'].values()

    element_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=element_name_[1],
        help_text=element_name_[0]
    )
    

    def clean(self):
        super.clean()
        if Element.objects.filter(element_name=self.element_name).exclude(pk=self.pk).exists():
            raise ValidationError({'element_name': 'An element with this name already exists'})

    def __str__(self)->str:
        return self.element_name
    
class ElementData(BaseModel):
    (
        _,
        element_value_,
    ) = HELP_TEXT_AND_VERBOSE_NAME['element'].values()
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    element_value = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=element_value_[1],
        help_text=element_value_[0]
    )

    def __str__(self):
        return f"{self.element.element_name}, {self.element_value} data for {self.plot.name}"

