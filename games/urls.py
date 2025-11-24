from django.urls import path
from .views import Game, GameDetailView

urlpatterns = [
    path("games/", Game.as_view(), name="created_game"),
    path("games/<int:game_id>/", GameDetailView.as_view(), name="game_detail"),
]
