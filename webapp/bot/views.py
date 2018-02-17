from django.shortcuts import render

from .forms import QueryForm
from .models import Response

import json
import os
import requests

import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '/../../scrapper'))

from footsie import Scrapper

# Create your views here.
def index(request):
    return render(request, 'index.html')

def footsie_intent(r)                
    # Check whether all required entities have been specified
    if r['result']['parameters']['company'] == '' or r['result']['parameters']['attribute'] == '':
        return r['result']['fulfillment']['speech']
    else:
        company_code = r['result']['parameters']['company']
        attribute = r['result']['parameters']['attribute']
        scrapper = Scrapper.Scrapper()
        company = scrapper.get_company_data(company_code)
        try:
            value = getattr(company.stock, attribute)
        except AttributeError:
            value = getattr(company, attribute)
        return 'The {} of {} is {}.'.format(attribute, company.name, value)

def sector_query_intent(r, is_sector):
    scraper = Scrapper.Scrapper()
    #if required entities have been specified get sector/sub-sector data
    if is_sector: #is a SectorQuery
        if r['result']['parameters']['sector'] == '' or r['result']['parameters']['sector_attribute'] == '':
            return r['result']['fulfillment']['speech']
        else:
            sector_name = r['result']['parameters']['sector']
            sector_attribute = r['result']['parameters']['sector_attribute']
            sector = scraper.get_sector_data(sector_name)
    else: #is a SubSectorQuery
        if r['result']['parameters']['subsector'] == '' or r['result']['parameters']['sector_attribute'] == '':
            return r['result']['fulfillment']['speech']
        else:
            sector_name = r['result']['parameters']['subsector']
            sector_attribute = r['result']['parameters']['sector_attribute']
            sector = scraper.get_sub_sector_data(sector_name)
    data = getattr(sector, sector_attribute)
    #form response
    if sector_attribute == "highest_price" or sector_attribute == "lowest_price": 
        return "{} has the {} {} in {}: {}".format(data.name, sector_attribute.split('_',1)[0], sector_attribute.split('_', 1)[1], sector_name, getattr(data.stock, sector_attribute.split('_', 1)[1]))
    elif sector_attribute == "news":
        response = ""
        for n in data:
            response += str(n)
        return response
    elif sector_attribute == "rising" or sector_attribute == "falling":
        if (len(data)==0):
            return "No companies in {} are {}".format(sector_name, sector_attribute)
        else:
            response = ""
            for company in data:
                if len(response) > 0: 
                    response += ","
                response += "{} is {}: {}%".format(company.name, sector_attribute, company.stock.per_diff)
            return response

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
                "timezone": "Africa/Casablanca"
            })

            r = requests.post(dialogflow_api, headers=headers, data=payload)
            r = r.json()
            response = {}
            if r['result']['action'] == "input.unknown":
                response['text'] = r['result']['fulfillment']['speech']
            else:
                if r['metadata']['intentName'] == 'Footsie Intent':
                    response['text'] = footsie_intent(r)
                elif r['metadata']['intentName'] == 'SectorQuery':
                    response['text'] = sector_query_intent(r, True)
                elif r['metadata']['intentName'] == 'SubSectorQuery':
                    response['text'] = sector_query_intent(r, False)  

            # reply = Response(query=query, response=json.dumps(response))
            # reply.save()

            form = QueryForm()
    else:
        form = QueryForm()

    return render(request, 'chat.html', {'form': form, 'response': response})
