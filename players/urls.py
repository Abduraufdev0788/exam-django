from django.urls import path
from .views import CreatePlayer

urlpatterns = [
    path('players/', CreatePlayer.as_view(), name='create_player'),
]