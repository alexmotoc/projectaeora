from django.shortcuts import render

from .forms import QueryForm

import json
import os
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def chat(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)

        if form.is_valid():
            question = form.cleaned_data['query']

            dialogflow_key = os.environ.get('DIALOGFLOW_CLIENT_ACCESS_TOKEN')
            dialogflow_api = 'https://api.dialogflow.com/v1/query?v=20150910'
            headers = {'Authorization': 'Bearer ' + dialogflow_key,
                       'Content-Type': 'application/json'}
            payload = json.dumps({
                "lang": "en",
                "query": question,
                "sessionId": "12345",
                "timezone": "Africa/Casablanca"
            })

            r = requests.post(dialogflow_api, headers=headers, data=payload)
            print(r.text)
            
            form = QueryForm()
    else:
        form = QueryForm()

    return render(request, 'chat.html', {'form': form})