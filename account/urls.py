from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('account.api.v1.urls'))
]
