#farm_data/serializers.py
from rest_framework import serializers
from django.db import transaction
from typing import List, Any, Dict
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
from farm_data.services.services_bulk_create import bulk_create_plot_data
from farm_data.selectors.selector_get_plot import get_plot




class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        exclude = ['status', 'plot_status']

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
    class Meta:
        model = ElementData
        exclude = ['status']
        list_serializer_class = ElementDataListSerializer


class PlotDetailSerializer(serializers.ModelSerializer):
    soil_data = SoilDataSerializer(source='soildata_set', read_only=True, many=True)
    environmental_data = EnvironmentalDataSerializer(source='environmentaldata_set', read_only=True, many=True)
    element_data = ElementDataSerializer(source='elementdata_set', read_only=True, many=True)
    plot_hardware = PlotHardWareDataSerializer(source='plothardwaredataset', read_only=True, many=True)

    class Meta:
        model = Plot
        fields = [
            'id', 'name', 'current_crop_type', 'soil_data', 'plot_status', 'last_sync_time', 
            'environmental_data', 'element_data', 'plot_hardware'
        ]

class SinglePlotSerializer(serializers.Serializer):
    plot_id = serializers.IntegerField(write_only=True)
    plot_hardware = PlotHardWareDataSerializer(many=True, write_only=True)
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
            'plot_hardware': result['plot_hardware_objects'],
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
            'plot_hardware': PlotHardWareDataSerializer(instance['plot_hardware'], many=True).data,
            'soil_data': SoilDataSerializer(instance['soil_data'], many=True).data,
            'environmental_data': EnvironmentalDataSerializer(instance['environmental_data'], many=True).data,
            'element_data': ElementDataSerializer(instance['element_data'], many=True).data,
        }