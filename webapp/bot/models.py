from django.db import models
from django.utils import timezone

class Query(models.Model):
    question = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} at {}'.format(question, str(created_at))


class Response(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    response = models.TextField()

    def __str__(self):
        return 'Q: {}\nA: {}'.format(self.query, self.response)
