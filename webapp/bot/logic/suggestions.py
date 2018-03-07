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
    'price': 'the price',
    'last_close_value': 'the last close value',
    'high': 'the current high',
    'sector': 'which sector it is in',
    'sub_sector': 'which sub-sector it is in'
}

sector_attributes = {
    'news': 'news',
    'highest_price': 'the highest price',
    'lowest_price': 'the lowest price',
    'rising': 'rising',
    'falling': 'falling',
    'performing': 'performance'
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


def get_sub_sectors(sector):
    sub_sectors = []
    for sector_element in sector_json:
        if sector_element == sector:
            for sub_sector in sector_json[sector]:
                sub_sectors.append(sub_sector)
            return sub_sectors


def get_sector_sub_sectors(sub_sector):
    sub_sectors = []
    for sector in sector_json:
        for sub_sector_element in sector_json[sector]:
            if sub_sector_element == sub_sector:
                for sub_sector_element in sector_json[sector]:
                    sub_sectors.append(sub_sector_element)
                return sector, sub_sectors


def add_suggestions(response, dialogflow_response):

    # if about a company
    if 'attribute' in dialogflow_response['result']['parameters']:
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

    # if a sector question
    elif 'sector_attribute' in dialogflow_response['result']['parameters']:

        if 'sector' in dialogflow_response['result']['parameters']:
            sector = dialogflow_response['result']['parameters']['sector']
            sub_sectors = get_sub_sectors(sector)
        else:
            sub_sector = dialogflow_response['result']['parameters']['subsector']
            sector, sub_sectors = get_sector_sub_sectors(sub_sector)

        sector_attribute = dialogflow_response['result']['parameters']['sector_attribute']  

        suggestions = []

        attributes = sector_attributes.copy()
        del attributes[sector_attribute]

        if 'sector' in dialogflow_response['result']['parameters']:
            for i in range(min(2, len(sub_sectors))):
                suggestion = random.choice(sub_sectors)
                sub_sectors.remove(suggestion)
                suggestions.append("What about {}?".format(suggestion))

            for i in range(4 - len(suggestions)):
                suggestion = random.choice(list(attributes.keys()))
                del attributes[suggestion]
                suggestions.append("What about {}?".format(sector_attributes[suggestion]))
        else:
            suggestions.append("What about {}?".format(sector))

            sub_sectors.remove(sub_sector)

            for i in range(min(2, len(sub_sectors))):
                print('test')
                suggestion = random.choice(sub_sectors)
                sub_sectors.remove(suggestion)
                suggestions.append("What about {}?".format(suggestion))

            for i in range(4 - len(suggestions)):
                suggestion = random.choice(list(attributes.keys()))
                del attributes[suggestion]
                suggestions.append("What about {}?".format(sector_attributes[suggestion]))

        response["suggestions"] = suggestions
    # else about risers
    else:
        if dialogflow_response['result']['parameters']['rise_fall'] == "risers":
            response["suggestions"] = ['What about the top fallers?']
        elif dialogflow_response['result']['parameters']['rise_fall'] == "fallers":
            response["suggestions"] = ['What about the top risers?']

    return response
