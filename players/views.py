from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
import json
from django.views import View

from scores.models import Score
from .models import Player

class CreatePlayer(View):
    def post(self, request:HttpRequest)->JsonResponse:
        results = json.loads(request.body.decode())
        if isinstance(results, dict):
            results = [results]

        for result in results:
            nickname = result.get('nickname')
            country = result.get('country')

            if not nickname:
                return JsonResponse({"message":"nickname required"}, status=401)
            if len(nickname) > 50:
                return JsonResponse({"message":"nickname max 50 characters"}, status=401)
            if Player.objects.filter(nickname=nickname, country=country).exists():
                return JsonResponse({"message":"nickname already exists"}, status=401)
            
            if not country:
                return JsonResponse({"message":"country required"}, status=401)
            if len(country) > 50:
                return JsonResponse({"message":"country max 50 characters"}, status=401)
            
            newplayer = Player(
                nickname=nickname,
                country=country
            )
            newplayer.save()

            context = {
                "id": newplayer.id,
                "nickname": newplayer.nickname,
                "country": newplayer.country,
                "rating": newplayer.rating,
                "created_at": newplayer.created_at
            }

            return JsonResponse(context, status=201)
        
    def get(self, request: HttpRequest) -> JsonResponse:

        players = Player.objects.all()

        country = request.GET.get('country')
        min_rating = request.GET.get('min_rating')
        search = request.GET.get('search')

        if country:
            players = players.filter(country__iexact=country)
        
        if min_rating:
            try:
                min_rating = int(min_rating)
                players = players.filter(rating__gte=min_rating)
            except ValueError:
                return JsonResponse({"message": "min_rating must be integer"}, status=400)
        
        if search:
            players = players.filter(nickname__icontains=search)

        results = []
        for player in players:
            scores = Score.objects.filter(player=player)
            total_games = scores.count()
            wins = scores.filter(result='win').count()
            draws = scores.filter(result='draw').count()
            losses = scores.filter(result='loss').count()

            results.append({
                "id": player.id,
                "nickname": player.nickname,
                "country": player.country,
                "rating": player.rating,
                "total_games": total_games,
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "created_at": player.created_at.isoformat()
            })

        context = {
            "count": players.count(),
            "next": None,
            "previous": None,
            "results": results
        }

        return JsonResponse(context, status=200)
    
class PlayerDetail(View):
    def get(self, request: HttpRequest, player_id: int) -> JsonResponse:
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return JsonResponse({"message": "player topilmadi"}, status=404)

        scores = Score.objects.filter(player=player)
        total_games = scores.count()
        wins = scores.filter(result='win').count()
        draws = scores.filter(result='draw').count()
        losses = scores.filter(result='loss').count()

        context = {
            "id": player.id,
            "nickname": player.nickname,
            "country": player.country,
            "rating": player.rating,
            "total_games": total_games,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "created_at": player.created_at.isoformat()
        }

        return JsonResponse(context, status=200)
    
    def put(self, request: HttpRequest, player_id: int) -> JsonResponse:
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return JsonResponse({"message": "player topilmadi"}, status=404)

        data = json.loads(request.body.decode())
        nickname = data.get('nickname')
        country = data.get('country')

        if nickname:
            if len(nickname) > 50:
                return JsonResponse({"message": "nickname max 50 characters"}, status=401)
            if Player.objects.filter(nickname=nickname, country=country).exclude(id=player_id).exists():
                return JsonResponse({"message": "nickname already exists"}, status=401)
            player.nickname = nickname

        if country:
            if len(country) > 50:
                return JsonResponse({"message": "country max 50 characters"}, status=401)
            player.country = country

        player.save()

        context = {
            "id": player.id,
            "nickname": player.nickname,
            "country": player.country,
            "rating": player.rating,
            "total_games": Score.objects.filter(player=player).count(),
            "wins": Score.objects.filter(player=player, result='win').count(),
            "draws": Score.objects.filter(player=player, result='draw').count(),
            "losses": Score.objects.filter(player=player, result='loss').count(),
            "created_at": player.created_at.isoformat(),
            
        }

        return JsonResponse(context, status=200)
    
    def delete(self, request: HttpRequest, player_id: int) -> JsonResponse:
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return JsonResponse({"message": "player topilmadi"}, status=404)

        player.delete()

        return JsonResponse({"error": "Cannot delete player with game history. Player has 45 recorded games."}, status=200)


       


            







