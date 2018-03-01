import json
import random

sector_json = json.load(open('../scraper/data/sectors.json'))

company_attributes = {
    'last_close_date': 'the last close date',
    'diff': 'change',
    'per_diff': 'the percentage change',
    'revenue': 'revenue',
    'news': 'news',
    'offer': 'the current offer',
    'bid': 'bid',
    'low': 'the current low',
    'volume': 'the current volume',
    'market_cap': 'the market cap',
    'price': 'price',
    'last_close_value': 'the last close value',
    'high': 'the current high'
}

# What does sector or sub_sector attribute do!??


def get_sector(company_code):
    for sector in sector_json:
        for sub_sector in sector_json[sector]:
            for company in sector_json[sector][sub_sector]:
                if company == company_code:
                    return sector, sub_sector


def get_companies_in_sector(requested_sector):
    # returns list of codes of companies in the requested_sector
    companies_in_sector = list()
    for sector in sector_json:
        if sector == requested_sector:
            for sub_sector in sector_json[sector]:
                companies_in_sector += sector_json[sector][sub_sector]
            break

    return companies_in_sector


def add_suggestions(response, dialogflow_response):

    if not response['type'] == 'top':
        company_code = dialogflow_response['result']['parameters']['company']
        attribute = dialogflow_response['result']['parameters']['attribute']

        sector, sub_sector = get_sector(company_code)

        companies_in_sector = get_companies_in_sector(sector)

        companies_in_sector.remove(company_code)

        suggestions = []
        for i in range(2):
            if len(companies_in_sector) > 0:
                suggestion = random.choice(companies_in_sector)
                companies_in_sector.remove(suggestion)
                suggestions.append("What about {}?".format(suggestion))

        attributes = company_attributes.copy()
        del attributes[attribute]

        for i in range(4 - len(suggestions)):
            suggestion = random.choice(list(attributes.keys()))
            del attributes[suggestion]
            suggestions.append("What about {}?".format(company_attributes[suggestion]))

        response['suggestions'] = suggestions

    return response
