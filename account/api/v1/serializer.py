from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _



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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
