from django.urls import path
from .views import CreateScore

urlpatterns = [
    path('scores/', CreateScore.as_view(), name='create_score'),
]