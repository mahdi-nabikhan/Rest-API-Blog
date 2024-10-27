from django.urls import path
from blog.api.v1.views import *
urlpatterns = [
    path('post-list/', PostList.as_view(), name='post-list'),

]