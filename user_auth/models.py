#user_auth/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from common.models import BaseModel
from user_auth.services.serviceManager import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Dict, List




AUTH_PROVIDERS = {'facebook':'facebook', 'google':'google',
                  'twitter':'twitter', 'email':'email'}
                
HELP_TEXT_AND_VERBOSE_NAME: Dict[str, Dict[str, List[str]]] ={
    'user': {
        'email': ['Enter a valid email address', 'Email Address'],
        'first_name':['Enter your first name', 'First Name'],
        'last_name':['Enter your last name', 'Last Name'],
        'is_staff': ['A staff', 'staff'],
        'is_active': ['Is the user active?', 'Active'],
        'is_admin': ['Is the user an admin?', 'Admin'],
        'auth_provider': ['Authentication provider', 'Auth Provider'],
    }
}

class CustomUser(AbstractBaseUser, BaseModel, PermissionsMixin):
    """
    This is a custom user object
    """


    (
    email_,
    first_name_,
    last_name_,
    is_staff_,
    is_active_,
    is_admin_,
    auth_provider_,
    ) = HELP_TEXT_AND_VERBOSE_NAME["user"].values()

    email = models.EmailField(
        max_length=200,
        unique=True,
        help_text=email_[0],
        verbose_name=email_[1],)
    first_name = models.CharField(
        max_length=255,
        help_text=first_name_[0],
        verbose_name=first_name_[1],)
    last_name = models.CharField(
        max_length=255,
        help_text=last_name_[0],
        verbose_name=last_name_[1],)
    auth_provider = models.CharField(
        max_length=255, 
        blank=True,
        null = False, 
        help_text=auth_provider_[0],
        verbose_name=auth_provider_[1],
        default=AUTH_PROVIDERS.get('email'))    
    is_active = models.BooleanField(
        default=True,
        help_text=is_active_[0],
        verbose_name=is_active_[1],
        )
    is_admin = models.BooleanField(
        default=False,
        help_text=is_admin_[0],
        verbose_name=is_admin_[1],
        )
    is_staff = models.BooleanField(
        default=False,
        help_text=is_staff_[0],
        verbose_name=is_staff_[1],
        )

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None)->bool:
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label)->bool:
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_admin_member(self)-> bool:
        "Is the user a member of staff?"
        return self.is_admin
    

    def clean(self)-> str:
        super().clean()
        self.email = self.__class__.normalize_username(self.email)
    
    @classmethod
    def get_email_field_name(cls) -> str:
        return cls.EMAIL_FIELD
    
    @classmethod
    def normailize_username(cls, username: str)-> str:
        return username.lower()
    
    def tokens(self)->Dict[str, str]:
        """
        method to get token for each user
        """
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }