# farm_data/selector_get_plot_hardware.py
from farm_data.models import PlotHardWareData
from typing import List, Any


def get_plot_hardware_list() -> List[PlotHardWareData]:
    """
    Fetches all plots from the database.

    Returns:
        List[PlotHardWareData]: A list of PlotHardWareData objects representing all plots in the database.
    """
    return PlotHardWareData.objects.all()