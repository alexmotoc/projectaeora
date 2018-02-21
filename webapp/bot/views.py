from django.http import JsonResponse
from django.shortcuts import render

from .forms import QueryForm
from bot.logic import intents
from .models import Response

import json
import os
import requests

import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '/../../scraper'))

from footsie import Scraper

# Create your views here.
def index(request):
    return render(request, 'index.html')

def chat(request):
    history = Response.objects.all()
    response = {}

    if request.method == 'POST':
        form = QueryForm(request.POST)

        if form.is_valid():
            # query = form.save()
            question = form.cleaned_data['question']

            dialogflow_key = os.environ.get('DIALOGFLOW_CLIENT_ACCESS_TOKEN')
            dialogflow_api = 'https://api.dialogflow.com/v1/query?v=20150910'
            headers = {'Authorization': 'Bearer ' + dialogflow_key,
                       'Content-Type': 'application/json'}
            payload = json.dumps({
                "lang": "en",
                "query": question,
                "sessionId": "12345",
                "timezone": "Africa/Casablacontent_type='application/xhtml+xml'nca"
            })

            r = requests.post(dialogflow_api, headers=headers, data=payload)
            r = r.json()

            if r['result']['action'] == "input.unknown":
                response['text'] = r['result']['fulfillment']['speech']
            else:
                if r['result']['metadata']['intentName'] == 'Footsie Intent':
                    response['text'] = intents.footsie_intent(r)
                elif r['result']['metadata']['intentName'] == 'SectorQuery':
                    response['text'] = intents.sector_query_intent(r, True)
                elif r['result']['metadata']['intentName'] == 'SubSectorQuery':
                    response['text'] = intents.sector_query_intent(r, False)
                elif r['result']['metadata']['intentName'] == 'TopRisers':
                    response['text'] = intents.top_risers_intent(r)
            # reply = Response(query=query, response=json.dumps(response))
            # reply.save()

            form = QueryForm()
    else:
        form = QueryForm()

    if request.is_ajax():
        return JsonResponse({'response': response})
    else:
        return render(request, 'chat.html', {'form': form, 'history': history})

def settings(request):
    return render(request, 'settings.html')
