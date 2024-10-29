from django.urls import path
from .views import *
urlpatterns = [
    path('registratin/',RegistrationApiView.as_view())
]