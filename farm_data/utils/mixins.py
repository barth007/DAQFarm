from .validator import validate_non_negative, validate_range

class PlotValidationMixin:
    """
    Custom Mixin
    """
    def validate_batter_status(self, value: int)-> int:
        """
        validation for battery status
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_range(value, 0, 100, 'Battery status')

    def validate_solar_panel_voltage(self, value: int)-> int: 
        """
        validation for  solar panel voltage

        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_non_negative(value, 'Solar Panel Voltage')

    def validate_board_temperature(self, value: int)-> int:
        """
        validation for board temperature
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        MIN_TEMPERATURE = -20  
        MAX_TEMPERATURE = 85
        return validate_range( value, MIN_TEMPERATURE, MAX_TEMPERATURE, 'Board temperature')

class SoilDataValidationMixin:
    """
    Custom Mixin
    """
    def validate_moisture(self, value: int)-> int:
        """
        validation for moisture content of the soil
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_range(value, 0, 100, 'Moisture')
    
    def validate_ph_level(self, value: int)-> int:
        """
        validation for ph level
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_range(value, 0, 14, 'PH level')

    def validate_electrical_conductivity(self, value: int)-> int:
        """
        validation for electrical conductivity
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_non_negative(value, 'Electrical conductivity')
    
    def validate_exchangeable_acid(self, value):
        """
        validation for exchangeable acid
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_non_negative(value, 'Exchangeable acidity')
    

class EnvironmentalDataValidationMixin:
    """
    Custom Mixin
    """
    def validate_temperature(self, value: int)-> int:
        """
        validation for temperature
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_range(value, -50, 60, 'Temperature')

    def validate_humidity(self, value: int)-> int:
        """
        validation for humidity
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_range(value, 0, 100, 'Humidity')

    def validate_pressure(self, value: int)-> int:
        """
        validation for pressure
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_range(value, 300, 1100, 'Pressure')

    def validate_natural_gas(self, value: int)-> int:
        """
        validation for natural gas
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_non_negative(value, 'Natural gas concentration')

    def validate_sunlight(self, value: int)-> int:
        """
        validation for sunlight
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_non_negative(value, 'Sunlight intensity')

    def validate_air_quality(self, value):
        """
        validation for air quality
        
        Args:
            value: an integer
        return
            Returns an integer which is the the value
        """
        return validate_range(value, 0, 500, 'Air quality index')