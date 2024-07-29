from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from typing import Any, Optional

class CustomUserManager(BaseUserManager):
    """
    A custom manager for handling user creation.
    """
    def create_user(self, email: str, password: Optional[str]=None, **extra_fields: Any )-> Any:
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        try:
            user.full_clean()
        except ValidationError as e:
            raise ValueError(f'Error creating user: {e}')
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email: str, password: Optional[str]=None, **extra_fields)-> Any:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True. ')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)
