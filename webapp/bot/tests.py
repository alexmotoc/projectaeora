from django.urls import resolve
from django.test import TestCase
from bot.views import index


class IndexTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

