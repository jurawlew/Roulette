from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from Game.models import GamePlay
from Game.permissions import IsOwner
from Game.serializers import GameSerializer, GamePlaySerializer


class GamePlayView(generics.UpdateAPIView):
    """ Игра юзера """
    serializer_class = GamePlaySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsOwner,)
    http_method_names = ['post']

    def get_object(self):
        try:
            obj = GamePlay.objects.get(user=self.request.user)
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data.get('result'))


class GameRoundsView(generics.ListAPIView):
    """ Раунды (по количеству юзеров) """
    serializer_class = GameSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get_queryset(self):
        queryset = (
            GamePlay.objects.values('round')
                .annotate(users=Count('user'))
                .order_by('-round')
        )
        return queryset


class UserActivityView(generics.ListAPIView):
    """ Активность юзеров (по раундам) """
    serializer_class = GameSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get_queryset(self):
        queryset = (
            GamePlay.objects.values('user', 'round')
                .annotate(scrolling=Count('user__gamelog__id'))
                .order_by('-round')
        )
        return queryset
