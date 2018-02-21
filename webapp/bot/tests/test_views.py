from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse, resolve

from bot.views import index


class IndexViewTests(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_view_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')

        # TODO: Start the template for the landing page
        self.assertTrue(html.startswith('<html>'))

        # TODO: Fill this in once the landing page has been created.
        # Until then fail this test.
        self.fail("Implement the landing page")


class ChatViewTests(TestCase):

    def test_chat_view_loads(self):
        response = self.client.get(reverse('chat'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat.html')

    def test_chat_view_ajax(self):
        response = self.client.post(reverse('chat'), {'question': 'BT stock price'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('The price of BT', response.json()['response']['text'])
        self.assertEqual(response.status_code, 200)
