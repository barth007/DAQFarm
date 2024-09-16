from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import calendar
from farm_data.selectors.selector_get_average import get_average_soil_data_per_day, get_average_environmental_data_per_day
from typing import List, Dict, Any

class AverageDataPerDayView(APIView):
    """ 
    A view that returns the average data per day.
    Methods:
        - get: Retrieves the average data per day.
    Attributes:
        - soil_temperature: A list of dictionaries containing the average, maximum, and minimum soil temperature per day.
        - ph: A list of dictionaries containing the average, maximum, and minimum pH per day.
        - moisture: A list of dictionaries containing the average, maximum, and minimum moisture per day.
        - environmental_temperature: A list of dictionaries containing the average, maximum, and minimum environmental temperature per day.
        - humidity: A list of dictionaries containing the average, maximum, and minimum humidity per day.
        - pressure: A list of dictionaries containing the average, maximum, and minimum pressure per day.
    """
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Parameters:
            - request: The HTTP request object.
            - args: Additional positional arguments.
            - kwargs: Additional keyword arguments.
        Returns:
            - Response: The HTTP response object with the average data per
       """
        soil_data = get_average_soil_data_per_day()
        environmental_data = get_average_environmental_data_per_day()
         
        def order_days(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """
            Orders the data by day of the week.
            Args:
            data (list): A list of dictionaries containing day and other data.
            Returns:
            list: A list of dictionaries ordered by day of the week, excluding days with no data.
            """
        
            ordered_data = {day: None for day in calendar.day_name}
            for entry in data:
                day_name = entry['day'].strftime('%A')
                ordered_data[day_name] = entry
            return [ordered_data[day] for day in calendar.day_name if ordered_data[day] is not None]
            
       
        def format_data(data: List[Dict[str, float]], keys: Dict[str, str]) -> List[Dict[str, Dict[str, float]]]:
            """
            Formats the given data into a list of dictionaries containing average, maximum, and minimum values for each day.
            Args:
                data (list): The data to be formatted.
                keys (dict): A dictionary containing keys for average, maximum, and minimum values.
            Returns:
                list: A list of dictionaries containing formatted data for each day.
            """
            return [
                {
                    day['day'].strftime('%A'): {
                        'avg': day.get(keys['avg']),
                        'max': day.get(keys['max']),
                        'min': day.get(keys['min'])
                    }
                } for day in order_days(data)
            ]

        response_data = {
            'soil_temperature': format_data(soil_data, {'avg': 'avg_soil_temp', 'max': 'max_soil_temp', 'min': 'min_soil_temp'}),
            'ph': format_data(soil_data, {'avg': 'avg_ph', 'max': 'max_ph', 'min': 'min_ph'}),
            'moisture': format_data(soil_data, {'avg': 'avg_moisture', 'max': 'max_moisture', 'min': 'min_moisture'}),
            'environmental_temperature': format_data(environmental_data, {'avg': 'avg_environ_temp', 'max': 'max_environ_temp', 'min': 'min_environ_temp'}),
            'humidity': format_data(environmental_data, {'avg': 'avg_environ_humidity', 'max': 'max_environ_humidity', 'min': 'min_environ_humidity'}),
            'pressure': format_data(environmental_data, {'avg': 'avg_environ_pressure', 'max': 'max_environ_pressure', 'min': 'min_environ_pressure'}),
        }
        return Response(response_data, status=status.HTTP_200_OK)