from django.test import TestCase

from bot.models import Query, Response


class QueryModelTest(TestCase):

    def test_saving_and_retrieving_queries(self):
        first_query = Query()
        # A classic question for the first query...
        first_query.question = "What is the stock price of Barlcays?"
        first_query.save()

        second_query = Query()
        second_query.question = "What are the top risers?"
        second_query.save()

        saved_queries = Query.objects.all()
        self.assertEquals(saved_queries.count(), 2)

        first_saved_query = saved_queries[0]
        second_saved_query = saved_queries[1]

        self.assertEquals(first_saved_query.question, "What is the stock price of Barlcays?")
        self.assertEquals(second_saved_query.question, "What are the top risers?")

class ResponseModelTest(TestCase):

    def test_saving_and_retrieving_queries(self):
        # TODO: Potential for this method to be tidied up slightly

        first_response_object = Response()

        first_test_query = Query()
        first_test_query.question = "What is the stock price of Barlcays?"
        first_test_query.save()

        first_response_object.query = Query.objects.all()[0]
        first_response_object.response = "The current spot price is: ..."
        first_response_object.save()

        second_response_object = Response()

        second_test_query = Query()
        second_test_query.question = "Who are the top risers?"
        second_test_query.save()

        second_response_object.query = Query.objects.all()[1]
        second_response_object.response = "The top risers are: ..."
        second_response_object.save()

        saved_responses = Response.objects.all()
        self.assertEquals(saved_responses.count(), 2)
        first_saved_response = saved_responses[0]
        second_saved_response = saved_responses[1]

        self.assertEquals(first_saved_response.query.question, "What is the stock price of Barlcays?")
        self.assertEquals(first_saved_response.response, "The current spot price is: ...")

        self.assertEquals(second_saved_response.query.question, "Who are the top risers?")
        self.assertEquals(second_saved_response.response, "The top risers are: ...")





