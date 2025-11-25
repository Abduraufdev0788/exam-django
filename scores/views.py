from multiprocessing import context
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpRequest, JsonResponse
from .models import Score
from players.models import Player
from games.models import Games
import json

class CreateScore(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        
        data = json.loads(request.body.decode())
        if not isinstance(data, list):
            data = [data]

        results_list =[]
        for item in data:
            game_id = item.get('game')
            player_id = item.get('player')
            result = item.get('result')
            opponent_name = item.get('opponent_name', '')

            if not game_id or not player_id or not result:
                return JsonResponse({"message": "game, player and result are required"}, status=400)
            
            if result not in ['win', 'draw', 'loss']:
                return JsonResponse({"message": "invalid result value"}, status=400)
            
            game = get_object_or_404(Games, id=game_id)
            player = get_object_or_404(Player, id=player_id)

            points_map = {'win': 10, 'draw': 5, 'loss': 0}

            score = Score.objects.create(
                game=game,
                player=player,
                result=result,
                points=points_map[result],
                opponent_name=opponent_name
            )

            player.rating += points_map[result]
            player.save()

            results_list.append({
                "id": score.id,
                "game": {"id": game.id, "title": game.title},
                "player": {"id": player.id, "nickname": player.nickname},
                "result": score.result,
                "points": score.points,
                "opponent_name": score.opponent_name,
                "created_at": score.created_at
            })

        if len(results_list) == 1:
            return JsonResponse(results_list[0], status=201)
        return JsonResponse(results_list, safe=False, status=201)
    
    def get(self, request: HttpRequest) -> JsonResponse:
        scores = Score.objects.all()

        game_id  = request.GET.get("game_id ")
        player_id = request.GET.get("player_id")
        result = request.GET.get("result")

        if game_id:
            search = scores.filter(game__id=game_id)

        if player_id:
            search = scores.filter(player__id=player_id)
        
        if result:
            search = scores.filter(result = result)

        results = []

        for score in search:
            results.append({
                "id": score.id,
                "game":{
                    "id":score.game.id,
                    "title":score.game.title
                },
                "player":{
                    "id":score.player.id,
                    "nickname": score.player.nickname
                },
                "result": score.result,
                "points": score.points,
                "opponent_name":score.opponent_name,
                "created_at":score.created_at.isoformat()
            })
        
        context = {
            "count": len(results),
            "results": results
        }

        return JsonResponse(context, status=201)



            

            