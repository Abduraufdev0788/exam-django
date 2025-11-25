from django.urls import path
from .views import LeaderBoardView

urlpatterns = [
    path("", LeaderBoardView.as_view(), name="leader_board_view")
]
