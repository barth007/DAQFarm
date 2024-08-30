from django.db.models import Avg, Max, Min
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from farm_data.models import SoilData, EnvironmentalData
from typing import Dict, List

def get_average_soil_data_per_day() -> List[Dict[str, float]]:
    """
    This function returns the average soil data per day
    """
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    return SoilData.objects.filter(created_at__date__gte=last_7_days).annotate(day=TruncDay('created_at')).values('day').annotate(
        avg_soil_temp=Avg('soilTemperature'),
        max_soil_temp=Max('soilTemperature'),
        min_soil_temp=Min('soilTemperature'),
        avg_moisture=Avg('moisture'),
        max_moisture=Max('moisture'),
        min_moisture=Min('moisture'),
        avg_ph=Avg('phLevel'),
        max_ph=Max('phLevel'),
        min_ph=Min('phLevel')
    ).order_by('day')

def get_average_environmental_data_per_day() -> List[Dict[str, float]]:
    """
    This function returns the average environmental data per day
    """
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    return EnvironmentalData.objects.filter(created_at__date__gte=last_7_days).annotate(day=TruncDay('created_at')).values('day').annotate(
        avg_environ_temp=Avg('temperature'),
        max_environ_temp=Max('temperature'),
        min_environ_temp=Min('temperature'),
        avg_environ_pressure=Avg('pressure'),
        max_environ_pressure=Max('pressure'),
        min_environ_pressure=Min('pressure'),
        avg_environ_humidity=Avg('humidity'),
        max_environ_humidity=Max('humidity'),
        min_environ_humidity=Min('humidity')
    ).order_by('day')