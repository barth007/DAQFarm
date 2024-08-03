#farm_data/urls.py
from django.urls import path
from farm_data.views.views_plots import (
    PlotListCreateView,
    PlotRetrieveUpdateDestroyView,
    PlotDetailView,
    SinglePlotListCreateView,
    )
from farm_data.views.views_plot_hardware import PlotHardWareListCreateView
from farm_data.views.views_soil_data import (
    SoilDataListCreateView,
    SoilDataRetrieveUpdateView,
)
from farm_data.views.views_environmental_data import (
    EnvironmentalDataListCreateView,
    EnvironmentalDataRetrieveView
    )
from farm_data.views.views_element import (
    ElementListCreateView,
    ElementretrieveUpdateDestroyView
)
from farm_data.views.views_element_value import (
    ElementDataretrieveView,
    ElementDataListCreateView
)


urlpatterns = [
    path('plot/', PlotListCreateView.as_view(), name='plot-list-create'),
    path('general/', SinglePlotListCreateView.as_view(), name='plot-list-create'),
    path('plot/<int:pk>/', PlotRetrieveUpdateDestroyView.as_view(), name='plot-retrieve-update-destroy'),
    path('plot-detail/<int:id>/', PlotDetailView.as_view(), name='plot-detail'),
    path('hardware/', PlotHardWareListCreateView.as_view(), name='hardware-list-create'),
    path('soil-data/', SoilDataListCreateView.as_view(), name='soil-list-create'),
    path('soil-data/<int:pk>/', SoilDataRetrieveUpdateView.as_view(), name='soil-retrieve-update'),
    path('environ/', EnvironmentalDataListCreateView.as_view(), name='environmental-data-list-create'),
    path('environ/<int:pk>/', EnvironmentalDataRetrieveView.as_view(), name='environmental-data-retrieve'),
    path('elements/', ElementListCreateView.as_view(), name='elements-list-create'),
    path('elements/<int:pk>/', ElementretrieveUpdateDestroyView.as_view(), name='elements-retrieve'),
    path('element-data/', ElementDataListCreateView.as_view(), name='element-data-list-create'),
    path('element-data/<int:pk>/',  ElementDataretrieveView.as_view(), name='element-data-retrieve'),
    ]