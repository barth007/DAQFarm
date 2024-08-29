from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from farm_data.selectors.selector_get_average import get_average_soil_data_per_day, get_average_environmental_data_per_day

class AverageDataPerDayView(APIView):
    """
    This class is used to get the average data per day
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Parameters:
        - request: The HTTP request object.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.
        Returns:
        - Response: The HTTP response object with the average data per day.
        """
        soil_data = get_average_soil_data_per_day()
        environmental_data = get_average_environmental_data_per_day()
        response_data = {
            'soil_temperature': [{day['day'].strftime('%A'): day.get('avg_soil_temperature')} for day in soil_data],
            'ph': [{day['day'].strftime('%A'): day.get('avg_ph')} for day in soil_data],
            'moisture': [{day['day'].strftime('%A'): day.get('avg_moisture') for day in soil_data}],
            'environmental_temperature': [{day['day'].strftime('%A'): day.get('avg_temperature') for day in environmental_data}],
            'humidity': [{day['day'].strftime('%A'): day.get('avg_humidity')} for day in environmental_data],
            'pressure': [{day['day'].strftime('%A'): day.get('avg_pressure')} for day in environmental_data],
        }
        return Response(response_data, status=status.HTTP_200_OK)