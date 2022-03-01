from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class TestMyEndpoint(TestCase):
    def test_that_deal_endpoint_works(self):
        client = APIClient()

        # find the url using the 'name=' kwarg in urls.py
        url = reverse('deal', args=(123,))

        # get because it's a GET method
        response = client.get(url)

        # it should complete successful
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        # the json in the response should contain a 'card' key in the dictionary
        # this test should probably be updated if the 'card' is not being returned
        self.assertTrue('hand' in response_data)

        #test game is getting set up in GameState model
        test_data = {username:'test_user', deck:['J', 10, 'Q', 'A'], player_hand: 9, dealer_hand: 8}

        setup_game = GameState.objects.all()
        # the POST should have added data to the model
        self.assertEqual(len(setup_game), 1)

        # the data in the model should match what was sent
        setup_data = setup_game[0]
        self.assertEqual(setup_game.username, 'test_user')
        self.assertEqual(setup_game.deck, ['J', 10, 'Q', 'A'])
        self.assertEqual(setup_game.player_hand, 9)
        self.assertEqual(setup_game.dealer_hand, 8)

        #test deal is adding card to player's hand


