from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type a message'}),
                            label='', max_length=256)