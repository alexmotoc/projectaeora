from django.http import JsonResponse
from django.shortcuts import render

from .forms import QueryForm, UserPreferencesForm
from bot.logic import intents, replies
from .models import Response, UserPreferences

from collections import defaultdict

import json
import os
import requests

import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '/../../scraper'))

from footsie import Scraper
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    return render(request, 'index.html')

def chat(request):
    history = Response.objects.all()
    response = {}

    try:
        preferences = UserPreferences.objects.all().first()
    except:
        preferences = UserPreferences.objects.create()
        preferences.save()

    attributes = []

    for field in preferences._meta.get_fields():
        if field.get_internal_type() == 'BooleanField' \
           and field.name != 'voice' and getattr(preferences, field.name):
                attributes.append(field.name)

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
            intent = r['result']['metadata']['intentName']

            if r['result']['action'] == "input.unknown":
                response['text'] = r['result']['fulfillment']['speech']
                response['type'] = 'input.unknown'
                response['speech'] = r['result']['fulfillment']['speech']
            else:
                if 'Footsie' in intent:
                    response = intents.footsie_intent(r, preferences.days_old)
                elif 'SubSectorQuery' in intent:
                    response = intents.sector_query_intent(r, False, preferences.days_old)
                elif 'SectorQuery' in intent:
                    response = intents.sector_query_intent(r, True, preferences.days_old)
                elif 'TopRisers' in intent:
                    response = intents.top_risers_intent(r)
                elif 'Daily Briefing' in intent:
                    response = intents.daily_briefings_intent(preferences.companies,
                               preferences.sectors, attributes, preferences.days_old)

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
        preferences = User.Preferences.objects.create()
        preferences.save()

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

def get_voice_preference(request):
    preferences = UserPreferences.objects.all().first()

    return JsonResponse({"voice": preferences.voice})


def remove_duplicates(news_data):
    lastn = ""
    for n in news_data['LSE']:
        if lastn != "":
            if n.url == lastn.url:
                news_data['LSE'].remove(n)
        lastn = n
    lastn = ""
    for n in news_data['YAHOO']:
        if lastn != "":
            if n.url == lastn.url:
                news_data['YAHOO'].remove(n)
        lastn = n
    return news_data

def interests(request):
    try:
        preferences = UserPreferences.objects.all().first()
    except:
        preferences = UserPreferences.objects.create()
        preferences.save()
    news_timeframe = preferences.days_old
    companies = preferences.companies
    sectors = preferences.sectors
    scraper = Scraper.Scraper()
    company_news_data = defaultdict()
    company_news_data['LSE'] = list()
    company_news_data['YAHOO'] = list()
    #get news, data for tracked companies
    company_data = list()
    for company in companies.split(", "):
        if len(company) > 0:
            financial_news_data = scraper.get_financial_news_data(company)
            company_data.append(scraper.get_company_data(company))
            company_news_data['LSE'] = company_news_data['LSE'] + financial_news_data['LSE']
            company_news_data['YAHOO'] = company_news_data['YAHOO'] + financial_news_data['YAHOO']   
    sector_news_data = defaultdict()
    sector_news_data['LSE'] = list()
    sector_news_data['YAHOO'] = list()
    #get news, data for tracked sectors
    for sector in sectors.split(", "):
        if len(sector) > 0:
            sector_data = scraper.get_sector_data(sector)
            company_data = company_data + sector_data.companies
            sector_news_data['LSE'] += scraper.get_sector_data(sector).news['LSE']
            sector_news_data['YAHOO'] += scraper.get_sector_data(sector).news['YAHOO']
    #merge company and sector news, sort by date and remove duplicates
    all_news_data = defaultdict()
    all_news_data['LSE'] = list()
    all_news_data['YAHOO'] = list()
    all_news_data['LSE'] = company_news_data['LSE'] + sector_news_data['LSE']
    all_news_data['YAHOO'] = company_news_data['YAHOO'] + sector_news_data['YAHOO'] 
    all_news_data['LSE'].sort(key=lambda x: datetime.strptime(x.date, '%H:%M %d-%b-%Y'), reverse=True)   
    all_news_data['YAHOO'].sort(key=lambda x: datetime.strptime(x.date, '%H:%M %d-%b-%Y'), reverse=True)
    all_news_data = remove_duplicates(all_news_data)
    all_news = replies.news_reply(all_news_data, news_timeframe)
    #remove duplicates from company_data
    company_data.sort(key=lambda x: x.code, reverse=True)
    lastc = ""
    for c in company_data:
        if lastc != "":
            if c.code == lastc.code:
                company_data.remove(c)
        lastc = c
    #pass data to interests template        
    data = {'companies': company_data, 'all_news': all_news}
    return render(request, 'interests.html', data)