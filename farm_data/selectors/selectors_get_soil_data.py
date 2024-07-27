# farm_data/selector_get_soil_data.py
from farm_data.models import SoilData
from typing import List, Any


def get_soilData_list() -> List[SoilData] :
    """
    Fetches all SoilData  from the database.

    Returns:
        List[Plot]: A list of Plot objects representing all plots in the database.
    """
    return SoilData.objects.all()