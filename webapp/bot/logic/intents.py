from footsie import Scraper
from bot.logic import replies
from collections import defaultdict
from datetime import datetime, timedelta
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../../../scraper'))


def footsie_intent(r, days):
    """
    :param r: The JSON object received from Dialogflow where the intent is a 'Footsie Intent'
    :param days: An integer specifying the user's preference for how many days of news they want to see
    :return: A dictionary containing the layout of the card to be displayed
    """
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

        # if query asks for news use replies.news_reply
        if attribute == "news":
            date_period = r['result']['parameters']['date-period']
            # if user specified a news timeframe
            if date_period:
                # calculate how many days of news were requested
                start, end = date_period.split('/')
                start_date = datetime.strptime(start, '%Y-%m-%d')
                end_date = datetime.strptime(end, '%Y-%m-%d')
                difference = end_date.date() - start_date.date()
                return replies.news_reply(scraper.get_financial_news_data(company_code), difference.days)
            else:
                return replies.news_reply(scraper.get_financial_news_data(company_code), days)
        
        # else if the query asks for revenue data use replies.revenue_reply
        elif attribute == "revenue":
            company = scraper.get_company_data(company_code)
            return replies.revenue_reply(company, r['result']['parameters']['date-period'])

        # else use replies.company_reply
        else:
            company = scraper.get_company_data(company_code)
            return replies.get_company_reply(company, attribute)


def sector_query_intent(r, is_sector, days):
    """
    :param r: The JSON object received from Dialogflow where the intent is either a SectorQuery or a SubSectorQuery
    :param is_sector: Boolean value to specify whether query relates to a sector (True) or a sub-sector (False)
    :days: An integer specifying the user's preference for how many days of news they want to see
    :return: A dictionary containing the layout of the card to be displayed
    """
    scraper = Scraper.Scraper()
    sector = None
    # if required entities have been specified get sector/sub-sector data
    if is_sector:  # is a SectorQuery
        if r['result']['parameters']['sector'] == '' or r['result']['parameters']['sector_attribute'] == '':
            reply = {}
            reply['text'] = r['result']['fulfillment']['speech']
            reply['speech'] = r['result']['fulfillment']['speech']
            reply['type'] = 'incomplete'
            return reply
        else:
            sector_name = r['result']['parameters']['sector']
            sector_attribute = r['result']['parameters']['sector_attribute']
            sector = scraper.get_sector_data(sector_name)
    else:  # is a SubSectorQuery
        if r['result']['parameters']['subsector'] == '' or r['result']['parameters']['sector_attribute'] == '':
            reply = {}
            reply['text'] = r['result']['fulfillment']['speech']
            reply['speech'] = r['result']['fulfillment']['speech']
            reply['type'] = 'incomplete'
            return reply
        else:
            sector_name = r['result']['parameters']['subsector']
            sector_attribute = r['result']['parameters']['sector_attribute']
            sector = scraper.get_sub_sector_data(sector_name)
    # if query asks for news
    if sector_attribute == "news":
        date_period = r['result']['parameters']['date-period']
        # if the user specified a news timeframe
        if date_period:
            # calculate number of days of news that was requested
            start, end = date_period.split('/')
            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = datetime.strptime(end, '%Y-%m-%d')
            difference = end_date.date() - start_date.date()
            return replies.news_reply(sector.news, difference.days)
        else:
            return replies.news_reply(sector.news, days)
    else:
        return replies.sector_reply(sector, sector_attribute)


def top_risers_intent(r):
    """
    :param r: A JSON object received from Dialogflow
    :return: A dictionary containing the layout of the card to be displayed
    """
    response = {}
    
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
        else:  # get both
            risers = scraper.get_top5()
            fallers = scraper.get_top5(False)
            risers_response = replies.big_movers_card(risers)
            fallers_response = replies.big_movers_card(fallers, False)
            response['speech'] = risers_response['speech'] + ' ' + fallers_response['speech']
            response['type'] = 'risers&fallers'
            response['text'] = {'risers': risers_response['text'], 'fallers': fallers_response['text']}

    return response


def daily_briefings_intent(companies, sectors, attributes, days):
    """
    :param companies: Comma separated values in a string that specify which companies the daily briefing should contain
    :param sectors: Comma separated values in a string that specify which sectors the daily briefing should contain
    :param attributes: A list containing the attributes that the daily briefing should contain
    :param days: An integer specifying the users' preference for how many days of news they want to see
    :return: A dictionary containing the layout of the cards to be displayed
    """
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
