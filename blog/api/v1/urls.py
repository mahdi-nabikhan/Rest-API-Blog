from django.urls import path
from blog.api.v1.views import *

urlpatterns = [
    # API View
    path('category/', CategoryListCreate.as_view(), name='category'),
    path('post-list/', PostListCreation.as_view(), name='post-list'),
    path('post-detail/<int:pk>/', PostDetail.as_view(), name='post-detail'),

    # Generic View

]
