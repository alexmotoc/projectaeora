import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
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


class UserPreferences(models.Model):
    colour_scheme = models.CharField(default='indigo', max_length=40)

    companies = models.TextField(default='')
    sectors = models.TextField(default='')

    # The properties beneath are for if the user wants to receive them in their daily briefing.
    daily_high = models.BooleanField(default=True)
    daily_low = models.BooleanField(default=True)
    percentage_change = models.BooleanField(default=True)
    news = models.BooleanField(default=False)
    days_old = models.IntegerField(default=3, validators=[MaxValueValidator(14), MinValueValidator(1)]) # how old the news should be

    # Defaults to False = text, True = respond with voice.
    voice = models.BooleanField(default=False)
