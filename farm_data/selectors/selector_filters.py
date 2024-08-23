#farm_data/selectors/selector_filters.py
from typing import Dict, List
from django_filters import rest_framework as filters
from farm_data.models import SoilData, EnvironmentalData


class SoilDataFilter(filters.FilterSet):
    """
    This class is used to filter the soil temperature data
    """
    soil_temperature = filters.RangeFilter(field_name='soilTemperature')
    ph = filters.RangeFilter(field_name='phLevel')
    moisture = filters.RangeFilter(field_name='moisture')
    class Meta:
        """
        Meta class for the `selector_filters` module.

        Attributes:
            model (Model): The model class to which the filter is applied.
            fields (list): The list of fields to be included in the filter.
        """
        model = SoilData
        fields = ['plot']


class EnvironmentalDataFilter(filters.FilterSet):
    
    environ_temperature = filters.RangeFilter(field_name='temperature')
    environ_humidity = filters.RangeFilter(field_name='humidity')
    environ_pressure = filters.RangeFilter(field_name='pressure')
    class Meta:
        model = EnvironmentalData
        fields = ['plot']
