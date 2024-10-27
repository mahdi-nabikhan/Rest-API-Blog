from rest_framework import serializers
from blog.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'
