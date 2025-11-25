from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from games.models import Games
from scores.models import Score

class LeaderBoardView(View):
    def get(self, request:HttpRequest)->JsonResponse:
        game_id = request.GET.get("game_id")

        if not game_id:
            return JsonResponse({"message":"game_id required"}, status = 401)
        
        game = get_object_or_404(Games, id=game_id)

        scores = Score.objects.filter(game = game).exists()

        if not scores:
            return JsonResponse({"message":"404 not defound"}, status = 404)
        
        points_map = {"win": 10, "draw": 5, "lose": 0}
        
