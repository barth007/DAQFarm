from rest_framework import serializers
from .models import Plot, SoilData, EnvironmentalData, Element, ElementData, PlotHardWareData
from .utils.mixins import PlotValidationMixin, SoilDataValidationMixin, EnvironmentalDataValidationMixin




class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        exclude = ['status']

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

class ElementDataSerializer(serializers.ModelSerializer):
    # element_value = serializers.DecimalField(source='element-data.element_value', max_digits=5, decimal_places=2)
    class Meta:
        model = ElementData
        exclude = ['status']


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

class SinglePlotSerializer(serializers.ModelSerializer):
    soil_data = SoilDataSerializer(source='soildata_set')
    environmental_data = EnvironmentalDataSerializer(source='environmentaldata_set')
    element_data = ElementDataSerializer(source='elementdata_set')
    # plot_hardware = PlotHardWareDataSerializer(source='plothardwaredataset')

    class Meta:
        model = PlotHardWareData
        fields = [
            'plot', 'battery_status', 'solar_panel_voltage', 'board_temperature', 'soil_data',
            'environmental_data', 'element_data'
        ]