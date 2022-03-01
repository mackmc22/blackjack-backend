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
        self.assertEqual(len(response_data['hand']), 1)

        # lets call the endpoint again
        response = client.get(url)
        response_data = response.json()

        self.assertEqual(len(response_data['hand']), 2)

    def test_reset_endpoint(self):
        # 1. Call the deal endpoint (make sure there's a card in there)
        # 2. Call reset endpoint (and make sure it returns 200)
        # 3. Call the deal endpoint again (make sure theres only one card)        
        pass
