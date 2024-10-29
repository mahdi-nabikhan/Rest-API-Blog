from rest_framework import serializers
from account.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class RegistrationSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_2']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_2'):
            raise serializers.ValidationError('details:password do not match')

        try:
            validate_password(attrs.get('password'))

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'email': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password_2')
        return User.objects.create_user(**validated_data)
