from rest_framework import serializers
from blog.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_relative_api_url', read_only=True)

    # absolute_url = serializers.SerializerMethodField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Posts
        fields = (
            'id', 'title', 'content', 'category', 'status', 'created_at', 'published_at', 'snippet', 'relative_url',
            )

    # def get_absolute_url(self, obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.absolute_url)
