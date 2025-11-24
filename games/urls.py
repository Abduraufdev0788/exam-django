from django.urls import path
from .views import Game

urlpatterns = [
    path("games/", Game.as_view(), name="created_game")
]
