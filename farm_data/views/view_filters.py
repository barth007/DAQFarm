#farm_data/views/views_plots.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from farm_data.models import SoilData, EnvironmentalData
from farm_data.selectors.selector_filters import SoilDataFilter, EnvironmentalDataFilter

class AverageSoilDataView(APIView):

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Parameters:
        - request: The HTTP request object.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.
        Returns:
        - Response: The HTTP response object with the average soil temperature.
        """
        
        filtered_qs= SoilDataFilter(data=request.GET, queryset=SoilData.objects.all())
        averages = filtered_qs.qs.aggregate(
            avg_soil_temp=Avg('soilTemperature'),
            avg_moisture=Avg('moisture'),
            avg_ph=Avg('phLevel')
            )
        return Response(averages, status=status.HTTP_200_OK)
    

class AverageEvironmentalDataView(APIView):
    def get(self, request, *args, **kwargs):
        filtered_qs = EnvironmentalDataFilter(data=request.GET, queryset=EnvironmentalData.objects.all())
        averages = filtered_qs.qs.aggregate(
            avg_environ_temp= Avg('temperature'),
            avg_environ_pressure = Avg('pressure'),
            avg_environ_humidity= Avg('humidity')
        )
        return Response(averages, status=status.HTTP_200_OK)