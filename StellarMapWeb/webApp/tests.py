from django.test import TestCase
from django.urls import reverse

class SearchViewTestCase(TestCase):
    def test_search_view(self):
        # Issue a GET request to the search view
        response = self.client.get(reverse('webApp:search_view'))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the correct number of items
        self.assertEqual(len(response.context['items']), 0)

        # Issue a POST request to the search view with some search criteria
        response = self.client.post(reverse('webApp:search_view'), {'search_criteria': 'test'})

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the correct number of items
        self.assertGreater(len(response.context['items']), 0)
