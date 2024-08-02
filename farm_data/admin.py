from django.contrib import admin
from .models import (
    Plot,
    SoilData,
    PlotHardWareData,
    Element,
    ElementData,
    EnvironmentalData
)
admin.site.register(Plot)
admin.site.register(PlotHardWareData)
admin.site.register(SoilData)
admin.site.register(Element)
admin.site.register(ElementData)
admin.site.register(EnvironmentalData)