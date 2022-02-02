from django.db import models


class GameState(models.Model):
    username = models.TextField(null=True)
    deck = models.TextField(null=True)
    player_hand = models.TextField()
    dealer_hand = models.TextField(null=True)
