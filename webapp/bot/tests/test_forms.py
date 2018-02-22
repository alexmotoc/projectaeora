from django.test import TestCase
from bot.forms import QueryForm, FollowCompanyForm

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

class FollowCompanyFormTest(TestCase):

    def test_form_validation_for_blank_input(self):
        form = FollowCompanyForm()
        self.assertFalse(form.is_valid())

    def test_form_validation_for_valid_input(self):
        form = FollowCompanyForm(data={'company_code': 'BARC'})
        self.assertTrue(form.is_valid)

    def test_form_validation_for_no_company_code(self):
        form = FollowCompanyForm(data={'company_code': ''})
        self.assertFalse(form.is_valid())