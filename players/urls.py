from django.urls import path
from .views import CreatePlayer, PlayerDetail

urlpatterns = [
    path('players/', CreatePlayer.as_view(), name='create_player'),
    path('players/<int:player_id>/', PlayerDetail.as_view(), name='player_detail'),
]