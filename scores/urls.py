from django.urls import path
from .views import CreateScore, ScoreDetailView

urlpatterns = [
    path('scores/', CreateScore.as_view(), name='create_score'),
    path('scores/<int:score_id>/', ScoreDetailView.as_view(), name='score_detail'),
]