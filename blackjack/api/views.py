import json
import json
import random

from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from api.models import GameState


class BlackJackGame:
    deck_cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
                  10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A'
                  ]

    def __init__(self):
        random.shuffle(self.deck_cards)

    def deal(self):
        return self.deck_cards.pop()

    hand = []
    card_total = 0

    def calculate_cards(self, hand):
        self.card_total = 0

        self.sort_cards_save_to_cards(hand)

        for card in self.hand:
            if card in ['J', 'Q', 'K']:
                card = 10
            if card == 'A':
                if self.card_total > 10:
                    card = 1
                else:
                    card = 11

            self.card_total = card + self.card_total

        return self.card_total

    def sort_cards_save_to_cards(self, hand):
        non_aces = []
        all_aces = []

        for card in hand:
            if card == 'A':
                all_aces.append(card)
            else:
                non_aces.append(card)

        self.hand = non_aces + all_aces


@api_view(["GET", "POST", "PUT"])
def deal(request, id):
    # data = json.loads(request.body)
    # username = data['username']

    db_hand = []
    db_games = GameState.objects.filter(username='mackenzie').all()
    if len(db_games) == 0:
        # how do I get this into the hand that called the function?
        blackjack_game = BlackJackGame()
        card_dealt = blackjack_game.deal()
        db_hand.append(card_dealt)

        db_game = GameState.objects.create(username='mackenzie', deck=json.dumps(blackjack_game.deck_cards),
                                           player_hand=json.dumps(db_hand))
    else:
        # triggering if we have a game that we should deal from
        db_game = db_games[0]
        db_deck = json.loads(db_game.deck)
        blackjack_game = BlackJackGame()
        blackjack_game.deck_cards = db_deck
        card_dealt = blackjack_game.deal()
        db_game.deck = json.dumps(blackjack_game.deck_cards)

        db_hand = json.loads(db_game.player_hand)
        db_hand.append(card_dealt)
        db_game.player_hand = json.dumps(db_hand)

        db_game.save()

    # 1. fill out the definition of calculate cards
    score = blackjack_game.calculate_cards(db_hand)
    # 2. based on the score, how does it affect the two columns (active, winner)?
    if score >= 21:
        db_game.active = False
        db_game.winner = 'player'
        print(db_game.winner)

    # 3. DON'T FORGET TO CALL SAVE
    db_game.save()
    # 4. return the winner

    return JsonResponse(data={'hand': db_hand, 'score': score, 'winner': db_game.winner}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def restart_game(request, id):
    record = GameState.objects.get(username='mackenzie')
    record.delete()

    return HttpResponse(status=status.HTTP_200_OK)
