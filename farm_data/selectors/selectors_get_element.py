# farm_data/selector_get_element.py
from farm_data.models import Element
from typing import List, Any


def get_element_list() -> List[Element] :
    """
    Fetches all Element  from the database.

    Returns:
        List[Element]: A list of Element objects representing all elements in the database.
    """
    return Element.objects.all()