#services/services_create_user.py

from user_auth.models import CustomUser
from typing import Any

def create_user(**kwargs: Any)-> CustomUser:
    return CustomUser.objects.create_user(**kwargs)