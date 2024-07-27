from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from farm_data.serializers import PlotHardWareDataSerializer
from farm_data.selectors.selectors_get_plot_hardware import get_plot_hardware_list
from typing import Any

class PlotHardWareListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = get_plot_hardware_list()
    serializer_class = PlotHardWareDataSerializer



    def get(self, request: Request, *args: Any, **kwargs: Any )-> Response:
        """
        fetching a list of all plot hardware
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
       
        """
        return self.list(request, *args, **kwargs)
    
    def post(self, request: Request, *args: Any, **kwargs: Any)-> Response:
        """
        creating a plot hardware data
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        plot_data = serializer.data
        return Response({'plot_hardware': plot_data, 'message': 'Plot hardware created successfully'}, status=status.HTTP_201_CREATED)


