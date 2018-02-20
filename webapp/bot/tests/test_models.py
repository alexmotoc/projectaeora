from django.test import TestCase

from webapp.bot.models import Query


class QueryModelTest(TestCase):

    def test_saving_and_retrieving_queries(self):
        first_query = Query()
        # A classic question for the first query...
        first_query.question = "What is the stock price of Barlcays?"
        first_query.save()

        second_query = Query()
        second_query.question = "What are the top risers?"
        second_query.save()

        saved_items = Query.objects.all()
        self.assertEquals(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEquals(first_saved_item, "What is the stock price of Barlcays?")
        self.assertEquals(second_saved_item, "What are the top risers?")
