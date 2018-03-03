from collections import defaultdict
from datetime import datetime
import os

import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../../../scraper'))

from footsie import Scraper
from bot.logic import replies

from bot.logic import replies

def footsie_intent(r, days):
    # Check whether all required entities have been specified
    if r['result']['actionIncomplete']:
        reply = {}
        reply['text'] = r['result']['fulfillment']['speech']
        reply['speech'] = r['result']['fulfillment']['speech']
        reply['type'] = 'incomplete'
        return reply
    else:
        company_code = r['result']['parameters']['company']
        attribute = r['result']['parameters']['attribute']
        scraper = Scraper.Scraper()

        if attribute == "news":
            return replies.news_reply(scraper.get_financial_news_data(company_code), days)
        elif attribute == "revenue":
            company = scraper.get_company_data(company_code)
            return replies.revenue_reply(company)
        else:
            company = scraper.get_company_data(company_code)
            return replies.get_company_reply(company, attribute)

def sector_query_intent(r, is_sector, days):
    scraper = Scraper.Scraper()
    sector = None
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
    if sector_attribute == "news":
        return replies.news_reply(sector.news, days)
    else:
        return replies.sector_reply(sector, sector_attribute)

def top_risers_intent(r):
    if r['result']['parameters']['rise_fall'] == '':
        return r['result']['fulfillment']['speech']
    else:
        scraper = Scraper.Scraper()
        if r['result']['parameters']['rise_fall'] == "risers":
            risers = scraper.get_top5()
            response = replies.big_movers_card(risers)
        elif r['result']['parameters']['rise_fall'] == "fallers":
            fallers = scraper.get_top5(False)
            response = replies.big_movers_card(fallers, False)
        else: #get both
            risers = scraper.get_top5()
            fallers = scraper.get_top5(False)
            response = "Top Risers:\n"+ scraper.get_top5(True)
            response += "\nTop Fallers:\n" +scraper.get_top5(False)

    return response

def daily_briefings_intent(companies, sectors, attributes, days):
    scraper = Scraper.Scraper()

    companies_data = []

    if companies:
        for company in companies.split(", "):
            companies_data.append(scraper.get_company_data(company))

    sectors_data = []
    if sectors:
        for sector in sectors.split(", "):
            sectors_data.append(scraper.get_sector_data(sector))

    response = replies.daily_briefings(companies_data, sectors_data, attributes, days)

    return response
