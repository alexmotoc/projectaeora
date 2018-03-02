from django.test import TestCase
from bot.forms import QueryForm, UserPreferencesForm

class QueryFormTest(TestCase):

    def test_form_validation_for_blank_input(self):
        form = QueryForm()
        self.assertFalse(form.is_valid())

    def test_form_validation_for_blank_query(self):
        form = QueryForm(data={'question': ''})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_valid_query(self):
        form = QueryForm(data={'question': 'What is the stock price of Barclays?'})
        self.assertTrue(form.is_valid())

class UserPreferencesFormTest(TestCase):

    def test_form_validation_for_blank_input(self):
        form = UserPreferencesForm()
        self.assertFalse(form.is_valid())

#Both company and sector fields are marked as 'not required' so form should be valid without either one of them?
    def test_form_validation_for_blank_company(self):
        form = UserPreferencesForm(data={'company': '', 'sector': 'Banks'})
        self.assertTrue(form.is_valid())

    def test_form_validation_for_blank_sector(self):
        form = UserPreferencesForm(data={'company': 'BARC', 'sector': ''})
        self.assertTrue(form.is_valid())

    def test_form_validation_for_valid_company_and_sector(self):
        form = UserPreferencesForm(data={'sector': 'Banks', 'company': 'BARC'})
        self.assertTrue(form.is_valid())
