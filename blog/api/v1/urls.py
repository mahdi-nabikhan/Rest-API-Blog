from django.urls import path
from blog.api.v1.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', PostCRUDViewSet, basename='Posts')
router.register(r'category', CategoryCRViewSet, basename='Category')
urlpatterns = [
    # API View
    path('category/', CategoryListCreate.as_view(), name='category'),
    path('post-list/', PostListCreation.as_view(), name='post-list'),
    path('post-detail/<int:pk>/', PostDetail.as_view(), name='post-detail'),

    # Generic View
    path('post-list-generic/', PostListGeneric.as_view(), name='post-list-generic'),
    path('post-detail-generic/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('category/generic/', CategoryListCreateGeneric.as_view(), name='category-generic'),
]
urlpatterns += router.urls
