from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from farm_data.serializers import PlotSerializer, PlotDetailSerializer, SinglePlotSerializer
from farm_data.selectors.selector_get_plot import get_plot_list, get_plot
from django.core.exceptions import ObjectDoesNotExist
from typing import Any

class PlotListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = get_plot_list()
    serializer_class = PlotSerializer



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
        creating a plot data
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
        return Response({'plot': plot_data, 'message': 'Plot created successfully'}, status=status.HTTP_201_CREATED)


class PlotRetrieveUpdateDestroyView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = get_plot_list()
    serializer_class = PlotSerializer

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

    def patch(self, request: Request, *args: Any, **kwargs: Any)-> Response:
        """
        partially update a plot data
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        updated_data = serializer.data
        return Response({'plot_data': updated_data, 'message':'Update successful'}, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        """
        Save the updated instance.
        """
        serializer.save()

    def put(self, request: Request, *args: Any, **kwargs: Any)-> Response:
        """
        update a plot data
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
        """
        return self.update(request, *args, **kwargs)
    
    def delete(self, request: Request, *args: Any, **kwargs: Any)-> Response:
        """
        delete a plot data
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Plot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        """
        Perform the deletion of the object.
        """
        instance.delete()


class PlotDetailView(generics.RetrieveAPIView):
    queryset = get_plot_list()
    serializer_class = PlotDetailSerializer
    lookup_field = 'id'

    



class SinglePlotListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = get_plot_list()
    serializer_class = SinglePlotSerializer

    
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Creating plot related data for an existing plot
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
        """
        plot_id = request.data.get('plot_id')
        if not plot_id:
            return Response({'error': 'Plot ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            plot = get_plot(id=plot_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Plot not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data, context={'plot_id': plot_id})
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            plot = serializer.save()
            return Response({
                'plot': serializer.data,
                'message': 'Plot data created successfully'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)