#farm_data/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import Type, Any
from django.db.models import Model
from django.utils import timezone
from farm_data.models import (
    SoilData, 
    PlotHardWareData, 
    EnvironmentalData, 
    ElementData)



THRESHOLDS = {
    "pH": (5.5, 7.5),
    "moisture": (20, 50),
    "battStatus": (20, 100),
    "boardTemp":(27, 60),
    "electCond":(500, 5000),
    "nitrogen": (100, 200),
    "phosphorus":(15, 80),
    "potassium": (100, 200)
}

FIELD_MAPPING = {
    "phLevel": "pH",
    "moisture": "moisture",
    "batteryStatus": "battStatus",
    "boardTemperature": "boardTemp",
    "electricalConductivity": "electCond",
    "nitrogen": "nitrogen",
    "phosphorus": "phosphorus",
    "potassium": "potassium" 
}


@receiver(post_save, sender=None)
def farm_data_post_save(sender: Type[Model], created: bool, instance: Model, **kwargs: Any)->None:
    """
    This reciever, recieves a signal and updates 
    the last_sync_time field once an instance
    of the some models are created

    Args:
        sender: the model sending the signals
        created: A boolean of if an instance is created or not
        instance: the object created
        Kwargs: Any addition arguments needed at runtime
    return:
        None
    """
    if sender not in (EnvironmentalData, PlotHardWareData, SoilData, ElementData):
        return
    if not created:
        return
    if not hasattr(instance, 'plot'):
         raise AttributeError(f"{instance} has no related Plot")
    plot = instance.plot
    plot.last_sync_time = timezone.now()
    plot_status = "good"
    for field, threshold_key in FIELD_MAPPING.items():
        if  hasattr(instance, field):
            value = getattr(instance, field)
            min_value, max_value = THRESHOLDS[threshold_key]
            if value < min_value or value > max_value:
                plot_status = "warning"
                break
    plot.plot_status = plot_status
    plot.save(update_fields=['last_sync_time', 'plot_status'])