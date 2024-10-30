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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


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
    custom TokenObtainPerView create a jwt token
    """
    serializer_class = CustomObtainTokenSerializer


class ChangePassword(generics.UpdateAPIView):
    """
    send old password & new password1 & new password 2 and change the old password
    old password
    """
    permission_classes = [IsAuthenticated]
    model = User
    serializer_class = ChangePasswordSerializers
    queryset = User.objects.all()

    def get_object(self):
        obj = self.request.user

        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['wrong password']})
            self.object.check_password(serializer.data.get('new_password1'))
            self.object.save()
            return Response({'details': 'changing password successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
