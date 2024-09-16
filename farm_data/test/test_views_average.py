from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from datetime import datetime, timedelta
import zoneinfo
from decimal import Decimal

class AverageDataPerDayViewTest(TestCase):
    """
    Test case for the AverageDataPerDayView class.
    Methods:
    - setUp: Set up the test case.
    - test_get_average_data_per_day: Test the get_average_data_per_day method.
    """

    def setUp(self):
        """
        Set up the test case by initializing the APIClient.
        This method is called before each test method is executed.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """

        self.client = APIClient()
        self.maxDiff = None

    @patch('farm_data.views.views_average.get_average_soil_data_per_day')
    @patch('farm_data.views.views_average.get_average_environmental_data_per_day')
    def test_get_average_data_per_day(self, mock_get_env_data, mock_get_soil_data):
        """
        Test case for the 'get_average_data_per_day' API endpoint.
        This test case mocks the data for soil and environmental data and sends a GET request to the API endpoint.
        It asserts that the response status code is 200 (OK) and the response data matches the expected format.
        """

        mock_get_soil_data.return_value = [
            {'day': datetime(2024, 8, 16, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'avg_soil_temp': None, 
             'max_soil_temp': None, 'min_soil_temp': None, 'avg_ph': Decimal('9.75'), 
             'max_ph': Decimal('10'), 'min_ph': Decimal('9.5'), 'avg_moisture': Decimal('57.5'), 
             'max_moisture': Decimal('60'), 'min_moisture': Decimal('55')
             },
            {'day': datetime(2024, 8, 18, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'avg_soil_temp': None, 
             'max_soil_temp': None, 'min_soil_temp': None, 'avg_ph': Decimal('10'), 
             'max_ph': Decimal('10.5'), 'min_ph': Decimal('9.5'), 'avg_moisture': Decimal('60'), 
             'max_moisture': Decimal('65'), 'min_moisture': Decimal('55')
             }
        ]

        mock_get_env_data.return_value = [
            {'day': datetime(2024, 8, 16, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'avg_temperature': Decimal('35'), 
             'max_temperature': Decimal('36'), 'min_temperature': Decimal('34'), 'avg_humidity': Decimal('35'), 
             'max_humidity': Decimal('40'), 'min_humidity': Decimal('30'), 'avg_pressure': Decimal('400'), 
             'max_pressure': Decimal('405'), 'min_pressure': Decimal('395')
             }
        ]

        response = self.client.get('/api/average-data-per-day/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'soil_temperature': [
                {'Friday': {'avg': None, 'max': None, 'min': None}},
                {'Sunday': {'avg': None, 'max': None, 'min': None}}
            ],
            'ph': [
                {'Friday': {'avg': Decimal('9.75'), 'max': Decimal('10'), 'min': Decimal('9.5')}},
                {'Sunday': {'avg': Decimal('10'), 'max': Decimal('10.5'), 'min': Decimal('9.5')}}
            ],
            'moisture': [
                {'Friday': {'avg': Decimal('57.5'), 'max': Decimal('60'), 'min': Decimal('55')}},
                {'Sunday': {'avg': Decimal('60'), 'max': Decimal('65'), 'min': Decimal('55')}}
            ],
            'environmental_temperature': [
                {'Friday': {'avg': Decimal('35'), 'max': Decimal('36'), 'min': Decimal('34')}}
            ],
            'humidity': [
                {'Friday': {'avg': Decimal('35'), 'max': Decimal('40'), 'min': Decimal('30')}}
            ],
            'pressure': [
                {'Friday': {'avg': Decimal('400'), 'max': Decimal('405'), 'min': Decimal('395')}}
            ]
        })

    @patch('farm_data.views.views_average.get_average_soil_data_per_day')
    @patch('farm_data.views.views_average.get_average_environmental_data_per_day')
    def test_get_average_data_per_day_no_data(self, mock_get_env_data, mock_get_soil_data):
        """
        Test case for the 'get_average_data_per_day' API endpoint when there is no data available.
        This test case mocks the absence of soil and environmental data and sends a GET request to the API endpoint.
        It asserts that the response status code is 200 (OK) and the response data is empty.
        """

        mock_get_soil_data.return_value = []
        mock_get_env_data.return_value = []

        response = self.client.get('/api/average-data-per-day/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'soil_temperature': [],
            'ph': [],
            'moisture': [],
            'environmental_temperature': [],
            'humidity': [],
            'pressure': []
        })

    @patch('farm_data.views.views_average.get_average_soil_data_per_day')
    @patch('farm_data.views.views_average.get_average_environmental_data_per_day')
    def test_get_average_data_per_day_missing_values(self, mock_get_env_data, mock_get_soil_data):
        """
        Test case for the 'get_average_data_per_day' API endpoint when some values are missing.
        This test case mocks the soil and environmental data with missing values and sends a GET request to the API endpoint.
        It asserts that the response status code is 200 (OK) and the response data contains the available values.
        """

        mock_get_soil_data.return_value = [
            {'day': datetime(2024, 8, 16, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'avg_soil_temp': None, 
             'max_soil_temp': None, 'min_soil_temp': None, 'avg_ph': Decimal('9.75'), 
             'max_ph': Decimal('10'), 'min_ph': Decimal('9.5'), 'avg_moisture': Decimal('57.5'), 
             'max_moisture': Decimal('60'), 'min_moisture': Decimal('55')
             },
            {'day': datetime(2024, 8, 18, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'avg_soil_temp': None, 
             'max_soil_temp': None, 'min_soil_temp': None, 'avg_ph': Decimal('10'), 
             'max_ph': Decimal('10.5'), 'min_ph': Decimal('9.5'), 'avg_moisture': Decimal('60'), 
             'max_moisture': Decimal('65'), 'min_moisture': Decimal('55')
             }
        ]

        mock_get_env_data.return_value = [
            {'day': datetime(2024, 8, 16, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'avg_temperature': Decimal('35'), 
             'max_temperature': Decimal('36'), 'min_temperature': Decimal('34'), 'avg_humidity': None, 
             'max_humidity': None, 'min_humidity': None, 'avg_pressure': Decimal('400'), 
             'max_pressure': Decimal('405'), 'min_pressure': Decimal('395')
             }
        ]

        response = self.client.get('/api/average-data-per-day/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'soil_temperature': [
                {'Friday': {'avg': None, 'max': None, 'min': None}},
                {'Sunday': {'avg': None, 'max': None, 'min': None}}
            ],
            'ph': [
                {'Friday': {'avg': Decimal('9.75'), 'max': Decimal('10'), 'min': Decimal('9.5')}},
                {'Sunday': {'avg': Decimal('10'), 'max': Decimal('10.5'), 'min': Decimal('9.5')}}
            ],
            'moisture': [
                {'Friday': {'avg': Decimal('57.5'), 'max': Decimal('60'), 'min': Decimal('55')}},
                {'Sunday': {'avg': Decimal('60'), 'max': Decimal('65'), 'min': Decimal('55')}}
            ],
            'environmental_temperature': [
                {'Friday': {'avg': Decimal('35'), 'max': Decimal('36'), 'min': Decimal('34')}}
            ],
            'humidity': [
                {'Friday': {'avg': None, 'max': None, 'min': None}}
            ],
            'pressure': [
                {'Friday': {'avg': Decimal('400'), 'max': Decimal('405'), 'min': Decimal('395')}}
            ]
        })
    
    @patch('farm_data.views.views_average.get_average_soil_data_per_day')
    @patch('farm_data.views.views_average.get_average_environmental_data_per_day')  
    def  test_get_average_data_per_day_last_7_days(
            self, 
            mock_get_env_data,
            mock_get_soil_data):
        today = datetime(2024, 8, 16, tzinfo=zoneinfo.ZoneInfo(key='UTC'))
        last_7_days = today - timedelta(days=7)
        print(last_7_days)
        mock_get_soil_data.return_value = [
            {'day': last_7_days + timedelta(days=1), 'avg_soil_temp': None, 'max_soil_temp': None, 'min_soil_temp': None, 
             'avg_ph': Decimal('9.75'), 'max_ph': Decimal('10'), 'min_ph': Decimal('9.5'), 
             'avg_moisture': Decimal('57.5'), 'max_moisture': Decimal('60'), 'min_moisture': Decimal('55')
            },
            {'day': last_7_days + timedelta(days=3), 'avg_soil_temp': None, 'max_soil_temp': None, 'min_soil_temp': None, 
             'avg_ph': Decimal('10'), 'max_ph': Decimal('10.5'), 'min_ph': Decimal('9.5'), 
             'avg_moisture': Decimal('60'), 'max_moisture': Decimal('65'), 'min_moisture': Decimal('55')
            }
        ]
        mock_get_env_data.return_value = [
            {'day': last_7_days + timedelta(days=1), 'avg_temperature': Decimal('35'), 'max_temperature': Decimal('36'), 
             'min_temperature': Decimal('34'), 'avg_humidity': Decimal('35'), 'max_humidity': Decimal('40'), 
             'min_humidity': Decimal('30'), 'avg_pressure': Decimal('400'), 'max_pressure': Decimal('405'), 
             'min_pressure': Decimal('395')
            }
        ]

        response = self.client.get('/api/average-data-per-day/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'soil_temperature': [
                {'Tuesday': {'avg': None, 'max': None, 'min': None}},
                {'Thursday': {'avg': None, 'max': None, 'min': None}}
            ],
            'ph': [
                {'Tuesday': {'avg': Decimal('9.75'), 'max': Decimal('10'), 'min': Decimal('9.5')}},
                {'Thursday': {'avg': Decimal('10'), 'max': Decimal('10.5'), 'min': Decimal('9.5')}
                }
            ],
            'moisture': [
                {'Tuesday': {'avg': Decimal('57.5'), 'max': Decimal('60'), 'min': Decimal('55')}},
                {'Thursday': {'avg': Decimal('60'), 'max': Decimal('65'), 'min': Decimal('55')}
                }
            ],
            'environmental_temperature': [
                {'Tuesday': {'avg': Decimal('35'), 'max': Decimal('36'), 'min': Decimal('34')}}
            ],
            'humidity': [
                {'Tuesday': {'avg': Decimal('35'), 'max': Decimal('40'), 'min': Decimal('30')}}
            ],
            'pressure': [
                {'Tuesday': {'avg': Decimal('400'), 'max': Decimal('405'), 'min': Decimal('395')}}
            ]
        })
        
