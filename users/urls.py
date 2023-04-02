
from django.urls import path, include
from rest_framework import routers
from users.views import UserAPIView, RegisterUserApiView, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm


app_name = 'users'

users_router = routers.SimpleRouter()
users_router.register('users', UserAPIView, basename="user")

urlpatterns = [
    path('', include(users_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterUserApiView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
