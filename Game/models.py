from django.db import models
from django.contrib.auth.models import User

from Roulette.settings import ROULETTE_JSON


def default_model_dict():
    return ROULETTE_JSON


class GamePlay(models.Model):
    """ Модель игры юзера """
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    roulette = models.JSONField(default=default_model_dict)
    round = models.IntegerField(default=0)


class GameLog(models.Model):
    """ Модель логов игр юзера """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    result = models.CharField()
