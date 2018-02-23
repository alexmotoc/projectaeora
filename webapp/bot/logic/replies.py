from collections import defaultdict

import json

def big_movers_card(top5, risers=True):
    """
    Returns a JSON object containing the layout of the big movers card tables.

    Keyword arguments:
    top5 - a list of tuples containing data about the top 5 companies
    risers - specified whether the list contains the risers (True) or fallers (False)
    """
    big_movers = defaultdict()

    # Build phrase for the voice output.
    category = 'risers' if risers else 'fallers'
    speech = 'The top 5 ' + category + ' are '
    companies = []

    for i in range(len(top5)):
        row = defaultdict()
        row['name'] = top5[i][0]
        row['price'] = top5[i][1]
        row['percentage_change'] = top5[i][2]

        speech += row['name']
        if i < len(top5) - 2:
            speech += ', '
        else:
            if i == len(top5) - 1:
                speech += '.'
            else:
                speech += ' and '

        companies.append(row)

    big_movers['speech'] = speech

    # Build elements for the card visualisation
    card = defaultdict()
    card['title'] = 'Top ' + category.title()
    card['companies'] = companies

    big_movers['text'] = card
    big_movers['type'] = 'top'

    return json.dumps(big_movers)


def news_reply(lse_list, yahoo_list):

    news = {"LSE": lse_list, "YAHOO": yahoo_list}
    overall_dict = {
        "speech": "Here are some news articles that I've found!",
        "type": "news",
        "text": news
    }

    return json.dumps(overall_dict, default=lambda o: o.__dict__, indent=4)

def get_company_reply(company, attribute):
    try:
        value = getattr(company.stock, attribute)
    except AttributeError:
        value = getattr(company, attribute)
    #related_attribute determines what related data will appear to complement the requested data
    related_attribute = {"bid": "offer", "offer": "bid", "sector": "sub_sector"
    , "sub_sector": "sector", "high": "low", "low" : "high", "diff": "per_diff"
    , "per_diff": "diff",  "last_close_value": "last_close_date"
    ,"last_close_date": "last_close_value", "revenue": "market_cap"
    ,"market_cap": "revenue", "volume" : "price", "price": "per_diff"}
    #to_english determines the english word that will be substituted for the attribute name
    to_english = {"bid": "bid", "offer": "offer", "sector": "sector", "sub_sector": "sub-sector", "high": "high", "low": "low", "diff": "change", "per_diff": "percentage change",
    "last_close_value": "last close", "last_close_date": "last close date", "revenue": "revenue", "market_cap": "market cap", "volume": "volume", "price": "price"}
    secondary_attribute = related_attribute[attribute]
    try:
        secondary_value = getattr(company.stock, secondary_attribute)
    except AttributeError:
        secondary_value = getattr(company, secondary_attribute)
    speech = "The "+to_english[attribute]+" of "+company.name+" is "+ value #The text to be spoken by the agent
    return str(json.dumps({'speech': speech,'text': {'name' : company.name,'code': company.code,'date': company.date,'primary': value,
    'secondary': secondary_value,'primary_type': attribute, 'secondary_type': secondary_attribute},"type": "company"}))
