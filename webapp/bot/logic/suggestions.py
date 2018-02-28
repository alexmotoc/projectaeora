import json
import random

sector_json = json.load(open('../scraper/data/sectors.json'))


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

    print(response)
    if not response['type'] == 'top':
        company_code = dialogflow_response['result']['parameters']['company']
        attribute = dialogflow_response['result']['parameters']['attribute']

        sector, sub_sector = get_sector(company_code)
        print("The sector is: {}".format(sector))

        companies_in_sector = get_companies_in_sector(sector)
        print("THE COMPANIES IN THE SECTOR ARE: ")
        print(companies_in_sector)
        print("THE COMPANY CODE IS {}".format(company_code))

        companies_in_sector.remove(company_code)

        suggested_companies = []
        for i in range(3):
            if len(companies_in_sector) > 0:
                suggestion = random.choice(companies_in_sector)
                companies_in_sector.remove(suggestion)
                suggested_companies.append("What about {}?".format(suggestion))

        other_actions = ["News"]

        suggestions = {'suggested_companies': suggested_companies, 'other_actions': other_actions}
        response['suggestions'] = suggestions

    return response
