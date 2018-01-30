from django.shortcuts import render

import json
import os
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def chat(request):
    dialogflow_key = os.environ.get('DIALOGFLOW_CLIENT_ACCESS_TOKEN')
    dialogflow_api = 'https://api.dialogflow.com/v1/query?v=20150910'
    headers = {'Authorization': 'Bearer ' + dialogflow_key,
               'Content-Type': 'application/json'}
    payload = json.dumps({
        "lang": "en",
        "query": "",
        "sessionId": "12345",
        "timezone": "Africa/Casablanca"
    })

    r = requests.post(dialogflow_api, headers=headers, data=payload)
    print(r.text)

    return render(request, 'chat.html')
