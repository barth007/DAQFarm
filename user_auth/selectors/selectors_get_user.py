#selectors/selectors_get_user_obj.py
from user_auth.models import CustomUser


def get_user_obj(obj: CustomUser) -> CustomUser:
    """
    Fetching a user istance
    """
    return CustomUser.objects.get(email=obj['email'])

def get_user_by_email(email: str)-> CustomUser:
    """
    Fetch user by email
    """
    return CustomUser.objects.filter(email=email)