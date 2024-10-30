from django.urls import path
from .views import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # registration
    path('registratin/', RegistrationApiView.as_view()),

    # token login
    path('token/login/', ObtainAuthToken.as_view(), name='token-login'),
    path('login/', Login.as_view(), name='login'),
    path('log_out/', CustomDiscardAuthToken.as_view(), name='token-logout'),

    # jwt login
    path('jwt/create/token/', TokenObtainPairView.as_view(), name='jwt-token'),
    path('jwt/refresh/token/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/token/', TokenVerifyView.as_view(), name='jwt-verify'),
    path('jwt/customLogin/',CustomTokenObtainPerView.as_view(),name='jwt-custom-login'),
]
