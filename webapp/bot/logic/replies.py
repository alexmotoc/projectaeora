from collections import defaultdict

#to_english determines the english word that will be substituted for the attribute name
to_english = {"bid": "bid", "offer": "offer", "sector": "sector", "sub_sector": "sub-sector",
"high": "high", "low": "low", "diff": "change", "per_diff": "percentage change",
"last_close_value": "last close", "last_close_date": "last close date", "revenue": "revenue",
"market_cap": "market cap", "volume": "volume", "price": "price"}

def big_movers_card(top5, risers=True):
    """
    Returns a dictionary containing the layout of the big movers card tables.

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

    return big_movers


def news_reply(financial_news):

    lse_news = []
    for news in financial_news['LSE']:
        row = {}
        row["date"] = news.date
        row["headline"] = news.headline
        row["url"] = news.url
        row["source"] = news.source
        row["impact"] = news.impact
        lse_news.append(row)

    yahoo_news = []
    for i in financial_news['YAHOO']:
        row = {}
        row["date"] = news.date
        row["headline"] = news.headline
        row["url"] = news.url
        row["source"] = news.source
        row["impact"] = news.impact
        yahoo_news.append(row)

    news = {"LSE": lse_news, "YAHOO": yahoo_news}
    overall_dict = {
        "speech": "Here are some news articles that I've found!",
        "type": "news",
        "text": news
    }

    return overall_dict


def get_company_reply(company, attribute):
    reply = defaultdict()

    try:
        value = getattr(company.stock, attribute)
    except AttributeError:
        value = getattr(company, attribute)

    #related_attribute determines what related data will appear to complement the requested data
    related_attribute = {"bid": "offer", "offer": "bid", "sector": "sub_sector"
    , "sub_sector": "sector", "high": "low", "low" : "high", "diff": "per_diff"
    , "per_diff": "diff",  "last_close_value": "last_close_date"
    ,"last_close_date": "last_close_value", "revenue": "market_cap"
    ,"market_cap": "volume", "volume" : "price", "price": "per_diff"}

    secondary_attribute = related_attribute[attribute]

    try:
        secondary_value = getattr(company.stock, secondary_attribute)
    except AttributeError:
        secondary_value = getattr(company, secondary_attribute)

    card = {'name' : company.name,'code': company.code,'date': company.date,'primary': value,
    'secondary': secondary_value,'primary_type': attribute, 'secondary_type': secondary_attribute}

    reply['text'] = card
    reply['type'] = 'company'
    reply['speech'] = "The " + to_english[attribute] + " of " + company.name + " is " + value #The text to be spoken by the agent

    return reply

def sector_reply(sector, sector_attribute):
    data = getattr(sector, sector_attribute)

    if (sector_attribute == "highest_price" or sector_attribute == "lowest_price"):
        data = getattr(sector, sector_attribute)
        sector_name = sector.name
        speech = "{} has the {} {} in {}: {}".format(data.name, sector_attribute.split('_',1)[0], sector_attribute.split('_', 1)[1], sector_name, getattr(data.stock, sector_attribute.split('_', 1)[1]))
        response = get_company_reply(data, "price")
        response['speech'] = speech
        return response
    elif sector_attribute == "rising" or sector_attribute == "falling":
        number_of_companies_in_sector = len(sector.companies)
        number_of_companies_moving_in_requested_direction = len(data)
        speech = ""
        if number_of_companies_moving_in_requested_direction == 0:
            speech = "No "+sector.name+" companies are "+sector_attribute+". "
            if sector_attribute == "rising":
                sector_attribute = "falling"
            else:
                sector_attribute = "rising"
            data = getattr(sector, sector_attribute)
        speech += "The following "+sector.name+" companies are "+sector_attribute+". "
        companies = []
        for i in range(len(data)):
            row = defaultdict()
            row['name'] = data[i].name
            row['price'] = data[i].stock.price
            row['percentage_change'] = data[i].stock.per_diff
            speech += row['name']
            if i < len(data) - 2:
                speech += ', '
            else:
                if i == len(data) - 1:
                    speech += '.'
                else:
                    speech += ' and '
            companies.append(row)
        movers = defaultdict()
        movers['speech'] = speech
        # Build elements for the card visualisation
        card = defaultdict()
        card['title'] = str(len(data))+'/'+str(number_of_companies_in_sector)+' '+sector.name+' are '+sector_attribute
        card['companies'] = companies
        movers['text'] = card
        movers['type'] = 'top'
        return movers

def revenue_reply(company):
    response = {}

    card = {}
    card['title'] = "Revenue Data for " + company.name
    card['revenue_data'] = list()

    response['speech'] = "Here is the revenue data for " + company.name
    response['type'] = "revenue"
    response['text'] = card

    for i in range(len(company.revenue)):
        row = {}
        row['date'] = company.revenue[i][0]
        row['revenue'] = company.revenue[i][1]
        card['revenue_data'].append(row)

    return response

def daily_briefings(companies, sectors, attributes):
    response = {}

    if not companies and not sectors:
        message = 'You are not currently tracking any companies or sectors. ' \
                  'Please add some in the settings page!'
        response['text'] = message
        response['speech'] = message
        response['type'] = 'error'
    elif not attributes:
        message = 'You have not selected any attributes to be displayed. ' \
                  'Please add some in the settings page!'
        response['text'] = message
        response['speech'] = message
        response['type'] = 'error'
    else:
        briefing = defaultdict()

        company_attributes = {"current_price": "price", "daily_high": "high", "daily_low": "low",
                             "percentage_change": "per_diff", "news": "news"}

        company_cards = []
        # Build company cards
        for company in companies:
            card = {'name': company.name, 'code': company.code, 'date': company.date}
            for attribute in attributes:
                attr = company_attributes[attribute]
                try:
                    value = getattr(company.stock, attr)
                except AttributeError:
                    value = getattr(company, attr)

                if attr == 'news':
                    card[attr] = news_reply(value)
                else:
                    card[attr] = value
            company_cards.append(card)

        briefing['companies'] = company_cards

        # Get sector news
        sector_attributes = ['highest_price', 'lowest_price', 'rising', 'falling']
        sector_cards = []

        for sector in sectors:
            card = {}

            for attribute in sector_attributes:
                card[attribute] = sector_reply(sector, attribute)

            # Check if user wants sector news
            if 'news' in attributes:
                card['news'] = news_reply(sector.news)

            sector_cards.append(card)

        briefing['sectors'] = sector_cards

        response['speech'] = 'Here is the latest information I could find!'
        response['text'] = briefing
        response['type'] = 'briefing'

    return response
