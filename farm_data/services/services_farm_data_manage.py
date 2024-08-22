from django.db import models
from django.db.models import Prefetch
from django.db.models import Q, F


THRESHOLDS = {
    "pH": (5.5, 7.5),
    "moisture": (20, 50),
    "battStatus": (20, 100),
    "boardTemp": (27, 60),
    "electCond": (500, 5000),
    # "nitrogen": (100, 200),
    # "phosphorus": (15, 80),
    # "potassium": (100, 200)
}

FIELD_MAPPING = {
    "soildata__phLevel": ("pH", "soildata__created_at"),  # Assuming 'created_at' exists
    "soildata__moisture": ("moisture", "soildata__created_at"),
    "plothardwaredata__batteryStatus": ("battStatus", "plothardwaredata__created_at"),
    "plothardwaredata__boardTemperature": ("boardTemp", "plothardwaredata__created_at"),
    "soildata__electricalConductivity": ("electCond", "soildata__created_at"),
    # "elementdata__nitrogen": "nitrogen",
    # "elementdata__phosphorus": "phosphorus",
    # "elementdata__potassium": "potassium" 
}

class PlotManager(models.Manager):
    def with_warning_status(self):
        return self.filter(plot_status="warning")
    def filter_plots_with_recent_warnings(self):
        from farm_data.models import SoilData, PlotHardWareData, EnvironmentalData

        # Get recent entries for related data
        recent_soil_data = SoilData.objects.order_by('-created_at').first()
        recent_hardware_data = PlotHardWareData.objects.order_by('-created_at').first()
        recent_environmental_data = EnvironmentalData.objects.order_by('-created_at').first()

        condition = Q()

        if recent_soil_data:
            min_ph, max_ph = THRESHOLDS["pH"]
            condition |= Q(soildata__phLevel__lt=min_ph) | Q(soildata__phLevel__gt=max_ph)

        if recent_hardware_data:
            min_batt, max_batt = THRESHOLDS["battStatus"]
            condition |= Q(plothardwaredata__batteryStatus__lt=min_batt) | Q(plothardwaredata__batteryStatus__gt=max_batt)

        if recent_environmental_data:
            min_temp, max_temp = THRESHOLDS["boardTemp"]
            condition |= Q(environmentaldata__temperature__lt=min_temp) | Q(environmentaldata__temperature__gt=max_temp)

        return self.filter(condition).distinct()
        