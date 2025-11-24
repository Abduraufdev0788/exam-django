from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
import json

from .models import Games

class Game(View):
    def post(self, request:HttpRequest)->JsonResponse:
        results = json.loads(request.body.decode())

        if isinstance(results, dict):
            results = [results]

        for result in results:

            title = result.get('title')
            location = result.get('location')
            start_date = result.get('start_date')
            description = result.get('description', '')

            if not title:
                return JsonResponse({"message":"title required"})
            if len(title) > 200:
                return JsonResponse({"message":"title max 200 characters"}, status = 401)
            
            if not location:
                return JsonResponse({"message":"location required"})
            if len(location) > 100:
                return JsonResponse({"message":"location max 100 characters"})
            
            if not start_date:
                return JsonResponse({"message":"start_date required"})
            

            new_game = Games(
                title = title,
                location = location,
                start_date = start_date,
                description = description
            )
            new_game.save()

            context = {
                "id": new_game.id,
                "title": new_game.title,
                "location": new_game.location,
                "start_date": new_game.start_date,
                "description": new_game.description,
                "created_at": new_game.created_at
            }

            return JsonResponse(context, status = 201)
    
class GameDetailView(View):
    def put(self, request:HttpRequest, game_id:int)->JsonResponse:

        game = get_object_or_404(Games, id = game_id)

        try:
            data = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        
        title = data.get("title")
        location = data.get("location")
        start_date = data.get("start_date")
        description = data.get("description")
        if title:
            if len(title)>200:
                return JsonResponse({"message": "title max 200 characters"}, status=400)
            game.title = title
        if location:
            if len(location) > 100:
                return JsonResponse({"message": "location max 100 characters"}, status=400)
            game.location = location
        
        if start_date:
            game.start_date = start_date
        if description:
            game.description = description

        game.save()

        context = {
                "id": game.id,
                "title": game.title,
                "location": game.location,
                "start_date": game.start_date,
                "description": game.description,
                "created_at": game.created_at
            }
        
        return JsonResponse(context, status = 201)









