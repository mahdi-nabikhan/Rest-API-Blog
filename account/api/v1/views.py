import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
import threading


class EmailThread(threading.Thread):
    """
    sending email use thread for separated  sending email with django
    """

    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()


class RegistrationApiView(generics.GenericAPIView):
    """
    get information from post request method and create a user
    information :
        email : char field
        password : char field
        password 2 : char field
    """
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            new = serializer.save()
            Token.objects.create(user=new)
            data = {
                'massage': 'user added',
                'email': serializer.validated_data['email'],

            }
            obj_user = get_object_or_404(User, email=serializer.validated_data['email'])
            token = self.get_token_for_user(obj_user)
            email_obj = EmailMessage('email/hello.tpl', {'name': 'ali'}, 'admin@admin.com', to=[self.email])
            EmailThread(email_obj).start()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class Login(ObtainAuthToken):
    """
    get information from post request method and give token (oauth token)
    information:
        email : char field
        password : char field

    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CustomDiscardAuthToken(APIView):
    """
    destroy user token (because we use o auth token) and log out
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'details': 'logged out'})


class CustomTokenObtainPerView(TokenObtainPairView):
    """
    custom creation token with TokenObtainPairView using CustomObtainTokenSerializer
    """
    serializer_class = CustomObtainTokenSerializer


class ChangePasswordAPIView(generics.UpdateAPIView):
    """
    get information for change password view for each user
    information:
        old_password = char field()
        new_password = char field()
        new_password1 = char field()
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'details': 'wrong password'})

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'details': 'changing password successfully'})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    """
    update and retrieve profile information:
    information:
        user foreign key from user table in account model
        first_name char field ()
        last_name char field ()
        description char field ()
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmailSendView(generics.GenericAPIView):
    """
    send a dummy email for testing ...
    """

    def get(self, request, *args, **kwargs):
        self.email = 'mitinabi718@gmail.com'
        obj_user = get_object_or_404(User, email=self.email)
        token = self.get_token_for_user(obj_user)
        email_obj = EmailMessage('email/hello.tpl', {'name': 'ali'}, 'admin@admin.com', to=[self.email])
        EmailThread(email_obj).start()
        return Response({'details': 'email sent'})

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationApiView(APIView):
    def post(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token['user_id']
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'expired token'})
        except jwt.InvalidTokenError:
            return Response({'detail': 'invalid token'})
        user = User.objects.get(pk=user_id)
        user.is_verified = True
        if user.is_verified:
            return Response({'detail': 'user already verified'})
        user.save()

        return Response({'detail': 'activated and verified'})


class ActivationResendApiView(APIView):
    serializer_class = ActivateResendSerializer

    def post(self, request, token, *args, **kwargs):
        email = request.data.get('email')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.validated_data.get('email')
            user = get_object_or_404(User, email=user_obj)
            token = self.get_token_for_user(user)
            email_obj = EmailMessage('email/hello.tpl', {'name': 'ali'}, 'admin@admin.com', to=[self.email])
            EmailThread(email_obj).start()
            return Response({'details': 'email sent'})
        else:
            return Response({'detail': 'email not found'})

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
