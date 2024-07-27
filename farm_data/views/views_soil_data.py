from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from farm_data.serializers import SoilDataSerializer
from farm_data.selectors.selectors_get_soil_data import get_soilData_list
from typing import Any


class SoilDataListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = get_soilData_list()
    serializer_class = SoilDataSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any )-> Response:
        """
        fetching a list of all plots
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
        creating a soil data
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
        soil_data = serializer.data
        return Response({'plot': soil_data, 'message': 'soil data created successfully'}, status=status.HTTP_201_CREATED)


class SoilDataRetrieveUpdateView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = get_soilData_list()
    serializer_class = SoilDataSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any)-> Response:
        """
        getting a plot data
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
        """
        return self.retrieve(request, *args, **kwargs)