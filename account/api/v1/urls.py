from django.urls import path
from .views import *
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('registratin/', RegistrationApiView.as_view()),
    path('token/login/', ObtainAuthToken.as_view(), name='token-login'),
    path('login/', Login.as_view(), name='login'),
    path('log_out/', CustomDiscardAuthToken.as_view(), name='token-logout')
]
