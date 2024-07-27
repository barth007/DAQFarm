#views/views_login.py
from rest_framework import viewsets, generics,permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from user_auth.serializers import LoginSerializer

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'user': serializer.data, 'message': "Login Successful"}, status=status.HTTP_200_OK)
