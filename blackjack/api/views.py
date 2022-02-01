import pdb
import json
import random

from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404


class Game():
    deck_cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
                  10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A'
                  ]

    def __init__(self):
        random.shuffle(self.deck_cards)


new_game = Game()


@api_view(["GET"])
def deal(request):
    dealt_card = Game.deck_cards.pop()
    return JsonResponse(data={'card': dealt_card}, status=status.HTTP_200_OK)
