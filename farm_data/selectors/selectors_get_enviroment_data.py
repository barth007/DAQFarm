# farm_data/selector_get_plot.py
from farm_data.models import EnvironmentalData
from typing import List, Any


def get_environmental_data_list() -> List[EnvironmentalData]:
    """
    Fetches all  Environmental Data from the database.

    Returns:
        List[EnvironmentalData]: A list of  Environmental Data objects representing all plots in the database.
    """
    return  EnvironmentalData.objects.all()