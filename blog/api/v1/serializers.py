from rest_framework import serializers
from blog.models import *
from account.models import *


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
            'author'
        )
        read_only_fields = ('author',)

    # def get_absolute_url(self, obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.absolute_url)

    def to_representation(self, instance):
        response = super(PostSerializer, self).to_representation(instance)
        request = self.context.get('request')
        print(request)
        if request.parser_context.get("kwargs").get("pk"):
            response.pop('snippet')
        else:
            response.pop('content')

        response['category'] = CategorySerializer(instance.category).data
        return response

    def create(self, validated_data):
        validated_data['author'] = User.objects.get(id=self.context.get('request').user.id)
        return super().create(validated_data)
