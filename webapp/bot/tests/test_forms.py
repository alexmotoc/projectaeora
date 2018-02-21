from django.test import TestCase
from bot.forms import QueryForm

class QueryFormTest(TestCase):

    def test_form_validation_for_blank_query(self):
        form = QueryForm(data={'question': ''})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_valid_query(self):
        form = QueryForm(data={'question': 'What is the stock price of Barclays?'})
        self.assertTrue(form.is_valid())