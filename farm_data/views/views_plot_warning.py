from rest_framework.views import APIView
from rest_framework.response import Response
from farm_data.models import Plot
from farm_data.serializers import PlotWarningSerializer

class PlotWarningsView(APIView):
    def get(self, request, *args, **kwargs):
        
        thresholds = {
            "phLevel": (5.5, 7.5),
            "moisture": (20, 50),
            "batteryStatus": (20, 100),
            "boardTemperature": (27, 60),
            "electricalConductivity": (500, 5000),
            # "nitrogen": (100, 200),
            # "phosphorus": (15, 80),
            # "potassium": (100, 200)
        }
        plots = Plot.objects.filter_plots_with_recent_warnings()
        
        serializer = PlotWarningSerializer(plots, many=True, context={'thresholds': thresholds})
        return Response(serializer.data)