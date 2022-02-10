import pdb
import json
import random

from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404

from api.models import GameState


class Game:
    deck_cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
                  10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A'
                  ]

    def __init__(self):
        random.shuffle(self.deck_cards)

    def deal(self):
        return self.deck_cards.pop()



@api_view(["GET", "POST", "PUT"])
def deal(request, id):


    #data = json.loads(request.body)
    #username = data['username']

    db_games = GameState.objects.filter(username='mackenzie').all()
    if len(db_games) == 0:
        # how do I get this into the hand that called the function?
        blackjack_game = Game()
        card_dealt = blackjack_game.deal()

        GameState.objects.create(username='mackenzie', deck=blackjack_game.deck_cards, player_hand=card_dealt,
                                 dealer_hand=None)
    else:
        db_game = db_games[0]
        card_dealt = db_game.deck.pop()


        #blackjack_game = Game()
        #blackjack_game.deck_cards = game.deck
        #card_dealt = blackjack_game.deal()

    return JsonResponse(data={'card': card_dealt}, status=status.HTTP_200_OK)
