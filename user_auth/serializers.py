#user_auth/serializer.py


from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from typing import Any, Dict
from user_auth.services.services_create_user import create_user
from user_auth.selectors.selectors_email_exists import is_email_exist
from user_auth.selectors.selectors_get_user import get_user_by_email, get_user_obj
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError




class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    class Meta:
        model= CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
    
    def validate_email(self, value: str) -> str:
        """
        check that email is unique and not empty
        """
        if not value:
            raise serializers.ValidationError("Email is required")
        elif is_email_exist(email=value):
            raise serializers.ValidationError("Email already exists.")
        
        return value
    
    def validate_first_name(self, value: str) -> str:
        """
        ensure first_name is not empty
        """
        if not value:
            raise serializers.ValidationError({"first_name":"First name is required"})
        return value
    
    def validate_last_name(self, value: str) -> str:
        """
        ensure last_name is not empty
        """
        if not value:
            raise serializers.ValidationError({"last_name":"Last name is required"})
        return value
    
    def validate_password(self, value: str) -> str:
        """
        ensure password is not empty
        """
        if not value:
            raise serializers.ValidationError({"password":"password is required"})
        return value
    
    def create(self, validated_data: Any) -> CustomUser:
        """
        creating user instance
        """
        try:
            return  create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"email": "Email already exists"})


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    tokens = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens']

    def get_tokens(self, obj: CustomUser)-> Dict[str, str]:
        """
        creating token
        """
        try:
            user = get_user_obj(obj)
            if user is None:
                raise AuthenticationFailed(detail="Invalid credentials, try again", code=401)
            return user.tokens()
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
    
    def validate(self, attrs: Dict[str, str])-> Dict[str, str]:
        email=attrs.get('email', '')
        password = attrs.get('password', '')
        # filter_user_email = get_user_by_email(email=email)s
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(detail="Invalid credentials, try again", code=401)
        if not user.is_active:
            raise AuthenticationFailed(detail="Account disabled", code=401)
        return {
            'email':user.email,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = { 
        'bad_token': ('Token is expired or invalid')
    }
    def validate(self, attrs: Dict)-> Dict:
        self.refresh_token = attrs['refresh']
        return attrs

    def save(self, **kwargs: Any)-> None:
        try:
            RefreshToken(self.refresh_token).blacklist()
        except TokenError:
            self.fail('bad_token')


    

