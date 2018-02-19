from django.test import TestCase
from django.urls import reverse

class ChatViewTests(TestCase):
    def test_chat_view_loads(self):
        response = self.client.get(reverse('bot:chat'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat.html')

    def test_chat_view_ajax(self):
        response = self.client.post(reverse('bot:chat'), {'question': 'BT stock price'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, 'BT stock price')
