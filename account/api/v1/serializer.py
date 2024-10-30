from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import User, Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
    email = serializers.EmailField(  # تغییر از username به email
        label=_("Email"),
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
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if user is None or not user.is_verified:
                raise serializers.ValidationError({'detail': 'Invalid credentials or user is not verified.'})

        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomObtainTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['user_id'] = self.user.id
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=250)
    new_password = serializers.CharField(max_length=250)
    new_password1 = serializers.CharField(max_length=250)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password1']:
            raise serializers.ValidationError({'details': 'password doesnt match'})

        try:
            validate_password(attrs.get('new_password1'))
        except exceptions.ValidationError as e:
            raise e

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'description')
        read_only_fields = ('user',)
