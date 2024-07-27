#views/views_register.py
from rest_framework import viewsets, generics,permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from user_auth.serializers import RegistrationSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response({'user': user_data, 'message': "User created successfully"}, status=status.HTTP_201_CREATED)