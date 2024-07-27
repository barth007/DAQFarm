# farm_data/selector_get_plot.py
from farm_data.models import Plot
from typing import List, Any


def get_plot_list() -> List[Plot]:
    """
    Fetches all plots from the database.

    Returns:
        List[Plot]: A list of Plot objects representing all plots in the database.
    """
    return Plot.objects.all()


