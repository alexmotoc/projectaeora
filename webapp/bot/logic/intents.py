import os

import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../../../scraper'))

from footsie import Scraper
from bot.logic import replies

from bot.logic import replies

def footsie_intent(r):
    # Check whether all required entities have been specified
    if r['result']['actionIncomplete']:
        return r['result']['fulfillment']['speech']
    else:
        company_code = r['result']['parameters']['company']
        attribute = r['result']['parameters']['attribute']
        scraper = Scraper.Scraper()

        if attribute == "news":
            return replies.news_reply(scraper.get_financial_news_data(company_code), scraper.get_yahoo_news_data(company_code))
        else:
            company = scraper.get_company_data(company_code)
            return replies.get_company_reply(company, attribute)

def sector_query_intent(r, is_sector):
    scraper = Scraper.Scraper()
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
