from django.http import JsonResponse
from django.shortcuts import render

from .forms import QueryForm, UserPreferencesForm
from bot.logic import intents
from .models import Response, UserPreferences

from collections import defaultdict

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
            query = form.save()
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

            response = defaultdict()

            # SubSector must come before Sector!

            if r['result']['action'] == "input.unknown":
                response['text'] = r['result']['fulfillment']['speech']
                response['type'] = 'input.unknown'
                response['speech'] = r['result']['fulfillment']['speech']
            else:
                if 'Footsie Intent' in r['result']['metadata']['intentName']:
                    response = intents.footsie_intent(r)
                elif 'SubSectorQuery' in r['result']['metadata']['intentName']:
                    response = intents.sector_query_intent(r, False)
                elif 'SectorQuery' in r['result']['metadata']['intentName']:
                    response = intents.sector_query_intent(r, True)

                elif r['result']['metadata']['intentName'] == 'TopRisers':
                    response = intents.top_risers_intent(r)
                else:
                    response['text'] = r['result']['fulfillment']['speech']
                    response['speech'] = r['result']['fulfillment']['speech']
                    response['type'] = 'simple.response'
            reply = Response(query=query, response=json.dumps(response))
            reply.save()

            form = QueryForm()
    else:
        form = QueryForm()

    if request.is_ajax():
        return JsonResponse(response)
    else:
        return render(request, 'chat.html', {'form': form, 'history': history})

def settings(request):
    status = None

    try:
        preferences = UserPreferences.objects.all().first()
    except:
        preferences = None

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=preferences)

        if form.is_valid():
            form.save()
            status = "Preferences saved!"
        else:
            status = "Preferences couldn't be saved!"
    else:
        form = UserPreferencesForm(instance=preferences)

    if request.is_ajax():
        return JsonResponse({"status": status})
    else:
        return render(request, 'settings.html', {'form': form})

def get_companies(request):
    saved_companies = []

    try:
        preferences = UserPreferences.objects.all().first()
        for company in preferences.companies.split(', '):
            if company:
                saved_companies.append({"name": company})
    except:
        preferences = None

    with open(os.path.dirname(__file__) + '/' + '/../../scraper/data/profiles.json') as f:
        companies = json.load(f)
        return JsonResponse({"companies": companies, "saved_companies": saved_companies})

def get_sectors(request):
    saved_sectors = []

    try:
        preferences = UserPreferences.objects.all().first()
        for sector in preferences.sectors.split(', '):
            if sector:
                saved_sectors.append({"name": sector})
    except:
        preferences = None

    with open(os.path.dirname(__file__) + '/' + '/../../scraper/data/sectors.json') as f:
        sectors = json.load(f)
        return JsonResponse({"sectors": sectors, "saved_sectors": saved_sectors})
