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


def get_plot(**kwargs: Any) -> 'Plot':
    """
    Retrieve a plot by its attributes.
    
    Args:
        **kwargs: Keyword arguments representing the attributes of the Plot to retrieve.
                  For example, id=1 would attempt to retrieve the Plot with ID 1.
                  
    Returns:
        Plot: The Plot object matching the given kwargs.
        
   
    """
    return Plot.objects.get(**kwargs)
    