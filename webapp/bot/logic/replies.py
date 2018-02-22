import json
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../../../scraper'))

from footsie import Scraper

scraper = Scraper.Scraper()


def obj_dict(obj):
    return obj.__dict__


def news_reply(company_code):
    overall_dict = {
        "London Stock Exchange": scraper.get_financial_news_data(company_code),
        "Yahoo News": scraper.get_yahoo_news_data(company_code)
                    }

    output_json = json.dumps(overall_dict, default=lambda o: o.__dict__, indent=4)

    return output_json