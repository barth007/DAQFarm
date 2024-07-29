#farm_data/services_bulk_create.py
from django.db import transaction
from typing import List, Dict, Any
from farm_data.models import (
    Plot,
    PlotHardWareData,
    SoilData,
    ElementData,
    EnvironmentalData
)

def bulk_create_plot_data(
    plot: Plot,
    plot_hardware_data: List[Dict[str, Any]],
    soil_data: List[Dict[str, Any]],
    environmental_data: List[Dict[str, Any]],
    element_data: List[Dict[str, Any]]
) -> Dict[str, List[Any]]:
    """
    Bulk create related data for a given plot within a single database transaction.

    Args:
        plot (Plot): The Plot instance to which the data is related.
        plot_hardware_data (list): A list of dictionaries containing data for PlotHardWareData.
        soil_data (list): A list of dictionaries containing data for SoilData.
        environmental_data (list): A list of dictionaries containing data for EnvironmentalData.
        element_data (list): A list of dictionaries containing data for ElementData.

    Returns:
        dict: A dictionary containing the created objects for each model.
    """
    
    with transaction.atomic():
        plot_hardware_objects = PlotHardWareData.objects.bulk_create([
            PlotHardWareData(plot=plot, **hardware) for hardware in plot_hardware_data
        ])

        soil_data_objects = SoilData.objects.bulk_create([
            SoilData(plot=plot, **soil) for soil in soil_data
        ])

        environmental_data_objects = EnvironmentalData.objects.bulk_create([
            EnvironmentalData(plot=plot, **env) for env in environmental_data
        ])

        element_data_objects = ElementData.objects.bulk_create([
            ElementData(plot=plot, **element) for element in element_data
        ])

    return {
        'plot_hardware_objects': plot_hardware_objects,
        'soil_data_objects': soil_data_objects,
        'environmental_data_objects': environmental_data_objects,
        'element_data_objects': element_data_objects,
    }