import pdb
import json
import random

from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404

from api.models import GameState


class Game():
    deck_cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
                  10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A'
                  ]

    def __init__(self):
        random.shuffle(self.deck_cards)


@api_view(["GET", "POST", "PUT"])
def deal(request, id):
    data = json.loads(request.body)
    username = data['username']
    deck = data['deck']
    player_hand = data['player_hand']
    dealer_hand = data['dealer-hand']

    # how do I get this into the hand that called the function?
    card_dealt = Game.deck_cards.pop()

    GameState.objects.create(username=username, deck=deck, player_hand=player_hand, dealer_hand=dealer_hand)

    return JsonResponse(data={'card': card_dealt}, status=status.HTTP_200_OK)
