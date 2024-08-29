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
from farm_data.views.views_plot_warning import PlotWarningsView
from farm_data.views.view_filters import AverageSoilDataView, AverageEvironmentalDataView
from farm_data.views.views_average import AverageDataPerDayView


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
    path('warning/', PlotWarningsView.as_view(), name='warning'),
    path('average-soil-data-filter/', AverageSoilDataView.as_view(), name='average-soil-data-filter'),
    path('average-environment-filter/', AverageEvironmentalDataView.as_view(), name='average-environment-filter'),
    path('average-data-per-day/', AverageDataPerDayView.as_view(), name='average-data-per-day')


    ]