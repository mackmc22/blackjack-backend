import pdb
import json

from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404

class Game:
    hand = []

    def deal(self):
        deck_cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
                      10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A'
                      ]

    def __init__(self):
        random.shuffle(self.deck_cards)

    def deal(self):
        return self.deck_cards.pop()

@api_view(["GET"])
def deal(request):
    return JsonResponse(data={'card': game.deal()}, status=status.HTTP_200_OK)