from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from farm_data.serializers import ElementDataSerializer
from farm_data.selectors.selectors_get_element_value import get_element_value_list
from typing import Any

class ElementDataListCreateView(generics.ListCreateAPIView):
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


    @swagger_auto_schema(
            request_body=ElementDataSerializer(many=True),
            responses={201: ElementDataSerializer(many=True)}
    )
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
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        element = serializer.data
        return Response({'name': element, 'message': 'Element data created successfully'}, status=status.HTTP_201_CREATED)


class ElementDataretrieveView(generics.RetrieveAPIView):
    queryset =get_element_value_list()
    serializer_class = ElementDataSerializer

    # def get(self, request: Request, *args: Any, **kwargs: Any)-> Response:
    #     """
    #     getting a element data
    #     Args:
    #         request- object making the post request
    #         args- positional arguments
    #         kwargs- key word arguments
    #     Return:
    #         return a response
    #     """
    #     return self.retrieve(request, *args, **kwargs)