from django import forms
from django.forms import ModelForm
from .models import Query, UserPreferences


class QueryForm(ModelForm):
    question = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type a message'}),
                            label='', max_length=256)

    class Meta:
        model = Query
        exclude = ['created_at']


class UserPreferencesForm(ModelForm):
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'autocomplete'}), required=False)
    sector = forms.CharField(widget=forms.TextInput(attrs={'class': 'autocomplete'}), required=False)

    class Meta:
        model = UserPreferences
        exclude = ['last_time_got_news']

