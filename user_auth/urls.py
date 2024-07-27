from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user_auth.views.views_register import RegisterView
from user_auth.views.views_login import LoginApiView
from user_auth.views.views_logout import LogoutAPIView

urlpatterns =[
    path('signup/', RegisterView.as_view(), name="signup"),
    path('signin/', LoginApiView.as_view(), name="sigin"),
    path('signout/', LogoutAPIView.as_view(), name="signout"),
]