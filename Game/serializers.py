import random

from django.db import transaction

from rest_framework import serializers

from Game.models import GamePlay, GameLog
from Roulette.settings import ROULETTE_JSON


class GameSerializer(serializers.ModelSerializer):
    """ Сериализатор игр для статической информации"""

    user = serializers.CharField(required=False)

    class Meta:
        model = GamePlay
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'scrolling' in instance:
            ret_extra = {'avg_scrolling': instance['scrolling'] / (instance['round'] + 1)}
            ret.update(ret_extra)
        if 'users' in instance:
            ret_extra = {'users': instance['users']}
            ret.update(ret_extra)
        return ret


class GamePlaySerializer(serializers.ModelSerializer):
    """ Сериализатор игры """

    user = serializers.HiddenField(read_only=False, default=serializers.CurrentUserDefault())
    result = serializers.CharField(required=False)

    class Meta:
        model = GamePlay
        fields = '__all__'

    def log_write(self, instance, result):
        log = GameLog.objects.create(user=instance.user)
        log.result = result
        log.save()
        return log

    @transaction.atomic
    def update(self, instance, validated_data):
        roulette = instance.roulette
        while len(roulette) != 0:
            nums = [key for key, value in roulette.items()]
            nums_weight = [value for key, value in roulette.items()]
            instance.result = random.choices(nums, nums_weight)[0]
            roulette.pop(instance.result)
            instance.roulette = roulette
            instance.save()
            self.log_write(instance=instance, result=instance.result)
            return instance
        else:
            instance.roulette = ROULETTE_JSON
            instance.round += 1
            instance.result = 'JackPot'
            instance.save()
            self.log_write(instance=instance, result='JackPot')
            return instance
