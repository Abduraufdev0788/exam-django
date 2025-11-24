from django.db import models

class Player(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50, unique=True)
    rating = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname}"
    
    def update_rating(self, delta: int):
        self.rating += delta
        self.save()