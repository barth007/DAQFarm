# farm_data/selector_get_element_value.py
from farm_data.models import ElementData
from typing import List, Any


def get_element_value_list() -> List[ElementData] :
    """
    Fetches all ElementData  from the database.

    Returns:
        List[ElementData]: A list of element data objects representing a plots in the database.
    """
    return ElementData.objects.all()