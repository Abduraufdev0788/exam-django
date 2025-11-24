from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
import json
from django.views import View
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


            







