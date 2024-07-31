from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from farm_data.serializers import ElementDataSerializer
from farm_data.selectors.selectors_get_element_value import get_element_value_list
from typing import Any

class ElementDataListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset =get_element_value_list()
    serializer_class = ElementDataSerializer


    def get(self, request: Request, *args: Any, **kwargs: Any )-> Response:
        """
        fetching a list of all element data
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
        creating a element data
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
        element = serializer.data
        return Response({'name': element, 'message': 'Element data created successfully'}, status=status.HTTP_201_CREATED)


class ElementDataretrieveView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset =get_element_value_list()
    serializer_class = ElementDataSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any)-> Response:
        """
        getting a element data
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
        """
        return self.retrieve(request, *args, **kwargs)