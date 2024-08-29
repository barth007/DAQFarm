from django.db.models import Avg
from django.db.models.functions import TruncDay
from farm_data.models import SoilData, EnvironmentalData
from typing import Dict, List

def get_average_soil_data_per_day() -> List[Dict[str, float]]:
    """
    This function returns the average soil data per day
    """
    return SoilData.objects.annotate(day=TruncDay('created_at')).values('day').annotate(
        avg_soil_temp=Avg('soilTemperature'),
        avg_moisture=Avg('moisture'),
        avg_ph=Avg('phLevel')
    ).order_by('day')

def get_average_environmental_data_per_day() -> List[Dict[str, float]]:
    """
    This function returns the average environmental data per day
    """
    return EnvironmentalData.objects.annotate(day=TruncDay('created_at')).values('day').annotate(
        avg_environ_temp=Avg('temperature'),
        avg_environ_pressure=Avg('pressure'),
        avg_environ_humidity=Avg('humidity')
    ).order_by('day')