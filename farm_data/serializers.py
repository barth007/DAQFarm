#farm_data/serializers.py
from rest_framework import serializers
from typing import List, Any, Dict
from farm_data.services.services_bulk_create import bulk_create_plot_data
from farm_data.selectors.selector_get_plot import get_plot
import logging
from .models import (
    Plot,
    SoilData,
    EnvironmentalData, 
    Element, 
    ElementData, 
    PlotHardWareData)
from .utils.mixins import (
    PlotValidationMixin, 
    SoilDataValidationMixin, 
    EnvironmentalDataValidationMixin)



logger = logging.getLogger(__name__)

class PlotSerializer(serializers.ModelSerializer):
    """
    """
    last_sync_calculated_time = serializers.SerializerMethodField()
    class Meta:
        model = Plot
        exclude = ['status', 'last_sync_time']
        read_only_fields = ['plot_status']

    def get_last_sync_calculated_time(self, obj: Plot)->str:
        return obj.last_sync_time_calculated

class PlotHardWareDataSerializer(serializers.ModelSerializer, PlotValidationMixin):
    class Meta:
        model = PlotHardWareData
        exclude = ['status']


class SoilDataSerializer(serializers.ModelSerializer, SoilDataValidationMixin):
    class Meta:
        model = SoilData
        exclude = ['status']

class EnvironmentalDataSerializer(serializers.ModelSerializer, EnvironmentalDataValidationMixin):
    class Meta:
        model = EnvironmentalData
        exclude = ['status']

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'

class ElementDataListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        representation = super().to_representation(data)
        return representation
class ElementDataSerializer(serializers.ModelSerializer):
    element_name = serializers.CharField(source='element.elementName', read_only=True)
    class Meta:
        model = ElementData
        # exclude = ['status']
        fields = ['element', 'element_name', 'elementValue', 'plot']
        list_serializer_class = ElementDataListSerializer


class PlotDetailSerializer(serializers.ModelSerializer):
    soil_data = SoilDataSerializer(source='soildata_set', read_only=True, many=True)
    environmental_data = EnvironmentalDataSerializer(source='environmentaldata_set', read_only=True, many=True)
    element_data = ElementDataSerializer(source='elementdata_set', read_only=True, many=True)
    plot_hardware = PlotHardWareDataSerializer(source='plothardwaredata_set', read_only=True, many=True)

    class Meta:
        model = Plot
        fields = [
            'id', 'name', 'current_crop_type', 'soil_data', 'plot_status', 'last_sync_time', 
            'environmental_data', 'element_data', 'plot_hardware'
        ]

class SinglePlotSerializer(serializers.Serializer):
    plot_id = serializers.IntegerField(write_only=True)
    plot_hardware_data = PlotHardWareDataSerializer(many=True, write_only=True)
    soil_data = SoilDataSerializer(many=True, write_only=True)
    environmental_data = EnvironmentalDataSerializer(many=True, write_only=True)
    element_data = ElementDataSerializer(many=True, write_only=True)

        

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and save plot-related data in bulk.

        Args:
            validated_data (dict): A dictionary of validated data containing plot 
            hardware, soil, environmental, and element data.

        Returns:
            dict: A dictionary containing the plot ID and lists of created objects 
            for plot hardware, soil data, environmental data, and element data.
        """
        plot_hardware_data = validated_data.get('plot_hardware', [])
        soil_data = validated_data.get('soil_data', [])
        environmental_data = validated_data.get('environmental_data', [])
        element_data = validated_data.get('element_data', [])

        plot_id = self.context['plot_id']
        plot = get_plot(id=plot_id)

        def remove_plot(data: List)->List:
            """
            Remove the 'plot' key from each dictionary in a list of dictionaries.

            Args:
                data (list): A list of dictionaries, where each dictionary may contain a 'plot' key.

            Returns:
                list: A new list of dictionaries, each excluding the 'plot' key if it was present.
            """
            return [{k: v for k, v in item.items() if k != 'plot'} for item in data]


        plot_hardware_data = remove_plot(plot_hardware_data)
        soil_data = remove_plot(soil_data)
        environmental_data = remove_plot(environmental_data)
        element_data = remove_plot(element_data)

        try:
            result = bulk_create_plot_data(
                plot, 
                plot_hardware_data, 
                soil_data, 
                environmental_data, 
                element_data)
        except Exception as e:
            raise serializers.ValidationError(f"Failed to save data: {str(e)}")
        return {
            'plot_id': plot_id,
            'plot_hardware_data': result['plot_hardware_data_objects'],
            'soil_data': result['soil_data_objects'],
            'environmental_data': result ['environmental_data_objects'],
            'element_data': result ['element_data_objects']
        }

    def to_representation(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert the instance into a dictionary representation.

        Args:
            instance (dict): A dictionary containing plot and related data instances.

        Returns:
            dict: A dictionary representation of the instance with serialized plot hardware, soil data, environmental data, and element data.
        """
        plot = get_plot(id=instance['plot_id'])
        return {
            'plot_id': instance['plot_id'],
            'plot_hardware_data': PlotHardWareDataSerializer(instance['plot_hardware_data'], many=True).data,
            'soil_data': SoilDataSerializer(instance['soil_data'], many=True).data,
            'environmental_data': EnvironmentalDataSerializer(instance['environmental_data'], many=True).data,
            'element_data': ElementDataSerializer(instance['element_data'], many=True).data,
        }
    


class PlotWarningSerializer(serializers.ModelSerializer):
    warnings = serializers.SerializerMethodField()
    last_sync_calculated_time = serializers.SerializerMethodField()

    class Meta:
        model = Plot
        fields = ['id', 'name', 'plot_status', 'warnings', 'last_sync_calculated_time']

    def get_warnings(self, obj):
        warnings = []
        logger.debug(f"Processing plot {obj.name} for warnings.")
        thresholds = self.context.get('thresholds', {})

        # if hasattr(obj, 'plothardwaredata_set'):
        #     min_temp, max_temp = thresholds.get('boardTemperature', (None, None))
        #     if min_temp is not None and obj.plothardwaredata_set.filter(boardTemperature__lt=min_temp).exists():
        #         warnings.append({
        #             "title": "Low Board Temperature",
        #             "message": f"The board temperature is below the safe threshold ({min_temp})."
        #         })
        #     elif max_temp is not None and obj.plothardwaredata_set.filter(boardTemperature__gt=max_temp).exists():
        #         warnings.append({
        #             "title": "High Board Temperature",
        #             "message": f"The board temperature is above the safe threshold ({max_temp})."
        #         })
        if hasattr(obj, 'soildata_set'):
            min_moisture, max_moisture = thresholds.get('moisture', (None, None))
            min_elec, max_elec = thresholds.get('electricalConductivity', (None, None))
            min_ph, max_ph = thresholds.get('phLevel', (None, None))
            if min_moisture is not None and obj.soildata_set.filter(moisture__lt=min_moisture).order_by('-created_at').first():
                warnings.append({
                    "title": "Low soil moisture",
                    "message": "Low soil moisture can lead to drought"
                })
            elif max_moisture is not None and obj.soildata_set.filter(moisture__gt=max_moisture).order_by('-created_at').first():
                warnings.append({
                    "title": "High soil moisture",
                    "message": "High soil moisture can lead to possible flood"
                })
            elif min_elec is not None and obj.soildata_set.filter(electricalConductivity__lt=min_elec).exists():
                warnings.append({
                    "title": "Low electrical conductivity",
                    "message":"This indicates a nutrient deficiencies"
                })
            elif max_elec is not None and obj.soildata_set.filter(electricalConductivity__gt=max_elec).exists():
                warnings.append({
                    "title":"High electrical conductivity",
                    "message": "This indicates an excess of salt in the soil"
                })
            elif min_ph is not None and obj.soildata_set.filter(phLevel__lt=min_ph).exists():
                warnings.append({
                    "title":"Low pH",
                    "message": "This can lead to decrease in soil nutrient"
                })
            elif max_ph is not None and obj.soildata_set.filter(phLevel__gt=max_ph).exists():
                warnings.append({
                    "title": "High pH",
                    "message": "This indicates a high acidicity in the soil"
                })
        if hasattr(obj, 'plothardwaredata_set'):
            min_batt, max_batt = thresholds.get('batteryStatus', (None, None))
            min_btemp, max_btemp = thresholds.get('boardTemperature', (None, None))

            if min_batt is not None and obj.plothardwaredata_set.filter(batteryStatus__lt=min_batt).exists():
                warnings.append({
                    "title": "Low battery",
                    "message": "Hardware may fail to stream"
                })
            elif max_batt is not None and obj.plothardwaredata_set.filter(batteryStatus__gt=max_batt).exists():
                warnings.append({
                    "title": "High battery",
                    "message": "battery is over full"

                })
            elif min_btemp is not None and obj.plothardwaredata_set.filter(boardTemperature__lt=min_btemp).exists():
                warnings.append({
                    "title": "Low board temperature",
                    "message": "Hardware box might be too damp"

                })
            elif max_btemp is not None and obj.plothardwaredata_set.filter(boardTemperature__gt=max_btemp).exists():
                warnings.append({
                    "title": "High board temperature",
                    "message": "board might get demaged"

                })

        return warnings
    def get_last_sync_calculated_time(self, obj):
        plot_serializer = PlotSerializer(obj)
        return plot_serializer.data.get('last_sync_calculated_time')