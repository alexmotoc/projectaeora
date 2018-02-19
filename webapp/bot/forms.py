from django import forms
from django.forms import ModelForm
from .models import Query, UserPreferences, FollowCompany


class QueryForm(ModelForm):
    question = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type a message'}),
                            label='', max_length=256)

    class Meta:
        model = Query
        exclude = ['created_at']


class UserPreferencesForm(ModelForm):

    class Meta:
        model = UserPreferences
        fields = '__all__'


class FollowCompanyForm(ModelForm):

    class Meta:
        model = FollowCompany
        exclude = ['sector', 'sub_sector', 'last_time_got_news']
