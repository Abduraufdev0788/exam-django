from django.db import models

class Score(models.Model):
    RESULT_CHOICES = (
        ('win', 'Win'),
        ('loss', 'Loss'),
        ('draw', 'Draw'),
    )
    game = models.ForeignKey('games.Games', on_delete=models.PROTECT, related_name='scores')
    player = models.ForeignKey('players.Player', on_delete=models.PROTECT, related_name='scores')
    result = models.CharField(max_length=10, choices=RESULT_CHOICES )
    points = models.IntegerField()
    opponent_name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
