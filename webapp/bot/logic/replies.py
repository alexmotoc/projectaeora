import os

import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../../../scraper'))

import json

from footsie import Scraper

scraper = Scraper.Scraper()

def obj_dict(obj):
    return obj.__dict__

def news_reply(company_code):
    news_list = scraper.get_financial_news_data(company_code)

    output_json = json.dumps(news_list, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    print(output_json)



news_reply("BARC")