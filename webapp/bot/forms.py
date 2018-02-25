from django import forms
from django.forms import ModelForm
from .models import Query

class QueryForm(ModelForm):
    question = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type a message'}),
                            label='', max_length=256)

    class Meta:
        model = Query
        exclude = ['created_at']
