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

    def calculate_cards(self, hand):
        card_total = 0

        hand = self.sort_cards_save_to_cards(hand)

        for card in hand:
            if card in ['J', 'Q', 'K']:
                card = 10
            if card == 'A':
                if card_total > 10:
                    card = 1
                else:
                    card = 11

            card_total = card + card_total

        return card_total

    def sort_cards_save_to_cards(self, hand):
        non_aces = []
        all_aces = []

        for card in hand:
            if card == 'A':
                all_aces.append(card)
            else:
                non_aces.append(card)

        return non_aces + all_aces


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

        if not db_game.active:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        db_deck = json.loads(db_game.deck)
        blackjack_game = BlackJackGame()
        blackjack_game.deck_cards = db_deck
        card_dealt = blackjack_game.deal()
        db_game.deck = json.dumps(blackjack_game.deck_cards)

        db_hand = json.loads(db_game.player_hand)
        db_hand.append(card_dealt)
        db_game.player_hand = json.dumps(db_hand)

        db_game.save()

    score = blackjack_game.calculate_cards(db_hand)

    if score == 21:
        db_game.active = False
        db_game.winner = 'player'
    if score > 21:
        db_game.active = False
        db_game.winner = 'dealer'

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


@api_view(["PUT"])
def stand(request, id):
    score = 0

    # find the existing game based on username
    db_games = GameState.objects.filter(username='mackenzie').all()
    db_game = db_games[0]
    # pull deck from GameState
    db_deck = json.loads(db_game.deck)
    # create new instance of the game
    blackjack_game = BlackJackGame()
    # load deck from GameState into new game instance
    blackjack_game.deck_cards = db_deck

    #considerign making this into an inner function?
    # deal card and add to dealer's hand
    card_dealt = blackjack_game.deal()
    db_dealer_hand = json.loads(db_game.dealer_hand)
    db_dealer_hand.append(card_dealt)
    db_game.dealer_hand = json.dumps(db_dealer_hand)
    db_player_hand = json.loads(db_game.player_hand)


    db_game.save()

    dealer_score = blackjack_game.calculate_cards(db_dealer_hand)

    while True:
        if dealer_score == 21:
            db_game.active = False
            db_game.winner = 'dealer'
            break

        if dealer_score > 21:
            db_game.active = False
            db_game.winner = 'player'
            break

        # if dealer's cards <16, dealer hits
        if dealer_score < 16:
            card_dealt = blackjack_game.deal()
            db_hand = json.loads(db_game.dealer_hand)
            db_hand.append(card_dealt)
            db_game.dealer_hand = json.dumps(db_hand)

            db_game.save()

            dealer_score = blackjack_game.calculate_cards(db_dealer_hand)

        if score >= 17:
            db_game.active = False
            player_score = blackjack_game.calculate_cards(db_player_hand)

            if player_score >= dealer_score:
                db_game.winner = 'player'
            else:
                db_game.winner = 'dealer'




        return JsonResponse(data={'hand': db_dealer_hand, 'score': dealer_score, 'winner': db_game.winner}, status=status.HTTP_200_OK)


