from django.urls import path

from Game.views import GamePlayView, GameRoundsView, UserActivityView

urlpatterns = [
    path('play', GamePlayView.as_view()),
    path('rounds', GameRoundsView.as_view()),
    path('activity', UserActivityView.as_view()),
]
