from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from farm_data.serializers import ElementSerializer
from farm_data.selectors.selectors_get_element import get_element_list
from typing import Any

class ElementListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset =get_element_list()
    serializer_class = ElementSerializer



    def get(self, request: Request, *args: Any, **kwargs: Any )-> Response:
        """
        fetching a list of all element
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
        creating a element 
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
        return Response({'name': element, 'message': 'Element created successfully'}, status=status.HTTP_201_CREATED)


class ElementretrieveUpdateDestroyView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset =get_element_list()
    serializer_class = ElementSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any)-> Response:
        """
        getting a element
        Args:
            request- object making the post request
            args- positional arguments
            kwargs- key word arguments
        Return:
            return a response
        """
        return self.retrieve(request, *args, **kwargs)

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
        return Response({"message": "Element deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        """
        Perform the deletion of the object.
        """
        instance.delete()