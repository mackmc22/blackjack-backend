from django.db import models


class GameState(models.Model):
    username = models.TextField()
    deck = models.TextField()
    player_hand = models.TextField()
    dealer_hand = models.TextField(null=True)
