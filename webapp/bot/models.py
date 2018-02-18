import datetime

from django.db import models
from django.utils import timezone


class Query(models.Model):
    question = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} at {}'.format(self.question, str(self.created_at))


class Response(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    response = models.TextField()

    def __str__(self):
        return 'Q: {}\nA: {}'.format(self.query, self.response)


class FollowCompany(models.Model):
    company_code = models.CharField(max_length=6)
    sector = models.CharField(max_length=40)
    sub_sector = models.CharField(max_length=40)

    # The properties beneath are for if the user wants to receive them in their daily briefing.
    current_price = models.BooleanField(default=True)
    daily_high = models.BooleanField(default=True)
    daily_low = models.BooleanField(default=True)
    percentage_change = models.BooleanField(default=True)
    news = models.BooleanField(default=False)
    news_image = models.BooleanField(default=False)

    # Record when the user last got news so that in the future, if they want news, they will only get news that they
    # haven't already seen,   
    last_time_got_news = models.DateField(datetime.date.today())