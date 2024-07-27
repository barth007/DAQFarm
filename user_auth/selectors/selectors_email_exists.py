#selectors/selectors_email_exist.py

from user_auth.models import CustomUser

def is_email_exist(email: str) ->bool:
    """
    checking if email exists
    """
    return CustomUser.objects.filter(email=email).exists()