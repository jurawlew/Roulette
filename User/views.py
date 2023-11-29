from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from User.serializers import UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    """ Регистрация юзера """
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']


class UserLoginView(generics.GenericAPIView):
    """ Логин юзера"""
    queryset = User.objects.all()
    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data.get('access')
        refresh = serializer.validated_data.get('refresh')

        if access is not None:
            response = Response(access, status=status.HTTP_200_OK)
            response.set_cookie('refresh', refresh, httponly=True, max_age=1209600, samesite=None)
            return response
        return Response({"Error": 'Oooops :( token problem'}, status=status.HTTP_400_BAD_REQUEST)
