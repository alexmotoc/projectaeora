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
    'high': 'the current high',
    'sector': 'which sector is it in',
    'sub_sector': 'which sub-sector is it in'
}

sector_attributes = {
    'news': 'news',
    'highest_price': 'the highest price',
    'lowest_price': 'the lowest price',
    'rising': 'rising',
    'falling': 'falling',
    'performing': 'performing'
}


def get_sector(company_code):
    """
    :param company_code: A company code for a FTSE 100 company.
    :return: The sector which the company is in.
    """
    for sector in sector_json:
        for sub_sector in sector_json[sector]:
            for company in sector_json[sector][sub_sector]:
                if company == company_code:
                    return sector, sub_sector


def get_companies_in_sector(requested_sector):
    """
    :param requested_sector: A sector that's in the FTSE100.
    :return: A list of company codes for all of the companies that are in requested_sector.
    """
    companies_in_sector = list()
    for sector in sector_json:
        if sector == requested_sector:
            for sub_sector in sector_json[sector]:
                companies_in_sector += sector_json[sector][sub_sector]
            break

    return companies_in_sector


def get_sub_sectors(sector):
    """
    :param sector: A sector that's in the FTSE100.
    :return: The sub-sectors that are in the specified sector.
    """
    sub_sectors = []
    for sector_element in sector_json:
        if sector_element == sector:
            for sub_sector in sector_json[sector]:
                sub_sectors.append(sub_sector)
            return sub_sectors


def get_sector_sub_sectors(sub_sector):
    """
    :param sub_sector: A sub-sector that's in the FTSE100.
    :return: The sector that the sub-sector is contained within and a list containing all of the sub-sectors that are
    within that sector.
    """
    sub_sectors = []
    for sector in sector_json:
        for sub_sector_element in sector_json[sector]:
            if sub_sector_element == sub_sector:
                for sub_sector_element in sector_json[sector]:
                    sub_sectors.append(sub_sector_element)
                return sector, sub_sectors


def add_suggestions(response, dialogflow_response):
    """
    :param response: A dictionary that contains the information which is to be passed to the front-end.
    :param dialogflow_response: The JSON response from dialogflow.
    :return: The response dictionary with a suggestions index, that contains a list of suggestions that are
    dependent on the intent of the query.
    """
    # if about a company
    if 'attribute' in dialogflow_response['result']['parameters']:
        company_code = dialogflow_response['result']['parameters']['company']
        attribute = dialogflow_response['result']['parameters']['attribute']

        sector, sub_sector = get_sector(company_code)

        companies_in_sector = get_companies_in_sector(sector)

        # remove the company that the user asked about from the list of companies in the sector
        companies_in_sector.remove(company_code)

        suggestions = []
        # add suggestions for other companies that are in the sector
        for i in range(2):
            if len(companies_in_sector) > 0:
                suggestion = random.choice(companies_in_sector)
                companies_in_sector.remove(suggestion)
                suggestions.append("What about {}?".format(suggestion))

        attributes = company_attributes.copy()
        # remove the attribute that the user asked about from the list of attributes
        del attributes[attribute]

        # add suggestions for other attributes.
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
        # remove the attribute that the user asked about from the list of attributes
        del attributes[sector_attribute]

        # if the user query was about a sector
        if 'sector' in dialogflow_response['result']['parameters']:
            # add suggestions for other sub-sectors that are in the sector
            for i in range(min(2, len(sub_sectors))):
                suggestion = random.choice(sub_sectors)
                sub_sectors.remove(suggestion)
                suggestions.append("What about {}?".format(suggestion))

            # add suggestions for other attributes
            for i in range(4 - len(suggestions)):
                suggestion = random.choice(list(attributes.keys()))
                del attributes[suggestion]
                suggestions.append("What about {}?".format(sector_attributes[suggestion]))

        # else the user's query was about a sub-sector
        else:
            suggestions.append("What about {}?".format(sector))

            # remove the sub-sector that the user asked about from the list of sub-sectors
            sub_sectors.remove(sub_sector)

            # add suggestions for other sub-sectors
            for i in range(min(2, len(sub_sectors))):
                suggestion = random.choice(sub_sectors)
                sub_sectors.remove(suggestion)
                suggestions.append("What about {}?".format(suggestion))

            # add suggestions for other attributes
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
