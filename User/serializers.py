from django.db import transaction
from django.contrib.auth.models import User

from rest_framework import serializers

from Game.models import GamePlay


class UserRegisterSerializer(serializers.ModelSerializer):
    """ Сериализатор регистрации юзера """

    class Meta:
        model = User
        fields = '__all__'

    def create_game(self, validated_data):
        try:
            return GamePlay.objects.create(user=validated_data)
        except BaseException as exc:
            return exc

    @transaction.atomic
    def create(self, validated_data):
        try:
            username = validated_data.pop('username')
            password = validated_data.pop('password')
            user = User.objects.create_user(username=username, password=password)
            self.create_game(validated_data=user)
            return user
        except BaseException as exc:
            return exc
