from collections import defaultdict
import html2text
from textblob import TextBlob
import requests
import bs4
import os
from datetime import datetime, timedelta


def get_stopwords():
    """
    :return: A list of stop words
    """
    # source=http://xpo6.com/list-of-english-stop-words/
    filepath = os.path.dirname(__file__) + '/stopwords.txt'
    stopwords = list()
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            stopwords.append(line.strip())
            line = fp.readline()
    return stopwords


def get_keywords(article):
    """
    :param article: A TextBlob of text to find the keywords from
    :return: A list of keywords from the text
    """
    stopwords = get_stopwords()
    words = article.words
    non_stopwords = list()
    for word in words:
        if word.lower() not in stopwords:
            non_stopwords.append(word.lower())
    words_sorted_by_frequency = sorted(non_stopwords, key=non_stopwords.count, reverse=True)
    keywords = set()
    for word in words_sorted_by_frequency:
        if len(keywords)<5:
            keywords.add(word.title())
        else:
            break
    return list(keywords)


def get_analysis(content):
    """
    :param content: A string with the text content to analyse
    :return: A string specifying the sentiment of the text
    :return: A list of the keywords in the text
    """
    blob = TextBlob(content)
    keywords = get_keywords(blob)

    if blob.sentiment.polarity > 0:
        sentiment = 'positive'
    elif blob.sentiment.polarity == 0:
        sentiment = 'neutral'
    else:
        sentiment = 'negative'

    return sentiment, keywords

# to_english determines the english word that will be substituted for the attribute name
to_english = {"bid": "bid", "offer": "offer", "sector": "sector", "sub_sector": "sub-sector",
              "high": "high", "low": "low", "diff": "change", "per_diff": "percentage change",
              "last_close_value": "last close", "last_close_date": "last close date", "revenue": "revenue",
              "market_cap": "market cap", "volume": "volume", "price": "price"}


def big_movers_card(top5, risers=True):
    """
    :param top5: A list of tuples containing data about the top 5 companies
    :param risers: Specify whether the list contains the risers (True) or fallers (False)
    :return: A dictionary containing the layout of the big movers card tables.
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


def news_reply(financial_news, days, positive_negative):
    """
    :param financial_news: A dictionary containing lists of LSE news and YAHOO news
    :param days: An integer specifying the number of days of news the response should contain
    :return: A dictionary containing the layout of the news cards
    """
    reply = defaultdict()
    # filter out LSE news that is too old
    lse_news = []
    for el in financial_news['LSE']:
        date = datetime.strptime(el.date, '%H:%M %d-%b-%Y')
        if date.date() >= datetime.now().date() - timedelta(days):
            row = {}
            row["date"] = el.date
            row["headline"] = el.headline
            row["url"] = el.url
            row["source"] = el.source
            row["impact"] = el.impact
            row["summary"] = "No summary is available."
            row["sentiment"] = "none"
            row["keywords"] = list()
            row["company"] = el.company
            lse_news.append(row)
    # filter out YAHOO news that is too old
    yahoo_news = []
    number_positive = number_neutral = number_negative = 0
    for i in financial_news['YAHOO']:
        date = datetime.strptime(i.date, '%H:%M %d-%b-%Y')
        if date.date() >= datetime.now().date() - timedelta(days):
            row = {}
            row["date"] = i.date
            row["headline"] = i.headline
            row["url"] = i.url
            row["source"] = i.source
            row["impact"] = i.impact
            row["summary"] = i.description[:256]
            if row["summary"][-3:] != "...":
                row["summary"] += "..."
            row["sentiment"], row["keywords"] = get_analysis(i.description)
            row["company"] = i.company
            yahoo_news.append(row)

            if row["sentiment"] == "positive":
                number_positive += 1
            elif row["sentiment"] == "neutral":
                number_neutral += 1
            else:
                number_negative += 1

    news = lse_news + yahoo_news
    news.sort(key=lambda x: datetime.strptime(x["date"], '%H:%M %d-%b-%Y'), reverse=True)

    if news:
        reply['speech'] = "Here are some news articles that I've found!"
        reply['type'] = 'news'
        reply['text'] = news

        if positive_negative:
            number_positive = 'no' if number_positive == 0 else number_positive
            number_neutral = 'no' if number_neutral == 0 else number_neutral
            number_negative = 'no' if number_negative == 0 else number_negative

            reply["positive_negative"] = "There are {} positive, {} neutral and {} negative articles.".format(
                number_neutral, number_positive, number_negative)
            reply['speech'] += " "
            reply['speech'] += reply['positive_negative']
    else:
        message = "I'm sorry, I couldn't find any recent articles. Try increasing the date period from the " \
                  "settings page or asking for an older date."
        reply['speech'] = message
        reply['type'] = "no-news"
        reply['text'] = message

    return reply


def get_company_reply(company, attribute):
    """
    :param company: A Company whose data was requested
    :param attribute: The attribute that the response should display the value of
    :return: A dictionary containing the layout of the company card
    """
    reply = defaultdict()

    try:
        value = getattr(company.stock, attribute)
    except AttributeError:
        value = getattr(company, attribute)

    # related_attribute determines what related data will appear to complement the requested data
    related_attribute = {"bid": "offer", "offer": "bid", "sector": "sub_sector",
                         "sub_sector": "sector", "high": "low", "low" : "high", "diff": "per_diff",
                         "per_diff": "diff",  "last_close_value": "last_close_date",
                         "last_close_date": "last_close_value", "revenue": "market_cap",
                         "market_cap": "volume", "volume" : "price", "price": "per_diff"}

    secondary_attribute = related_attribute[attribute]

    try:
        secondary_value = getattr(company.stock, secondary_attribute)
    except AttributeError:
        secondary_value = getattr(company, secondary_attribute)

    card = {'name' : company.name,'code': company.code,'date': company.date,'primary': value,
            'secondary': secondary_value,'primary_type': attribute, 'secondary_type': secondary_attribute}

    reply['text'] = card
    reply['type'] = 'company'
    reply['speech'] = "The " + to_english[attribute] + " of " + company.name + " is " + value

    return reply


def comparison_reply(company_data):
    reply = defaultdict()

    companies = []
    for i in range(len(company_data)):
        companies.append(get_company_reply(company_data[i], 'price'))

    if len(companies) == 1:
        reply['text'] = companies
        reply['type'] = 'comparison'
        reply['speech'] = "The price of {} is {}.".format(companies[0]['text']['name'], companies[0]['text']['primary'])
    else:
        reply['text'] = companies
        reply['type'] = 'comparison'
        reply['speech'] = 'Here is the side by side comparison of ' + company_data[0].name

        for i in range(1, len(company_data)):
            reply['speech'] += ' and {}'.format(company_data[i].name)

    return reply


def sector_reply(sector, sector_attribute):
    """
    :param sector: A Sector whose data was requested
    :param sector_attribute: The attribute that the response should show the value of
    :return: A dictionary containing the layout of either a 'company card'/'big movers card'/'news card'
    """
    data = getattr(sector, sector_attribute)

    if sector_attribute == "highest_price" or sector_attribute == "lowest_price":
        data = getattr(sector, sector_attribute)
        sector_name = sector.name
        speech = "{} has the {} {} in {}: {}".format(data.name, sector_attribute.split('_',1)[0],
                                                     sector_attribute.split('_', 1)[1], sector_name,
                                                     getattr(data.stock, sector_attribute.split('_', 1)[1]))
        response = get_company_reply(data, "price")
        response['speech'] = speech
        return response
    elif sector_attribute == "rising" or sector_attribute == "falling":
        number_of_companies_in_sector = len(sector.companies)
        number_of_companies_moving_in_requested_direction = len(data)

        if number_of_companies_moving_in_requested_direction == 0:
            speech = "No "+sector.name+" are "+sector_attribute+". "
        else:
            speech = "The following "+sector.name+" companies are "+sector_attribute+". "
        companies = []

        # Build table of data
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
        if number_of_companies_moving_in_requested_direction == 0:
            movers['text'] = speech
            movers['type'] = 'no-data'
        else:
            movers['text'] = card
            movers['type'] = 'top'

        return movers
    elif sector_attribute == "performing":
        companies = []
        for i in range(len(data)):
            row = defaultdict()
            row['name'] = data[i].name
            row['price'] = data[i].stock.price
            row['percentage_change'] = data[i].stock.per_diff
            companies.append(row)
        movers = defaultdict()
        movers['speech'] = "Here is some data about how "+sector.name+" are performing"
        card = defaultdict()
        card['title'] = "Performance of "+sector.name
        card['companies'] = companies
        movers['text'] = card
        movers['type'] = 'top'
        return movers    
    elif sector_attribute == "companies":
        companies = []
        for i in range(len(data)):
            row = defaultdict()
            row['name'] = data[i].name
            companies.append(row)
        movers = defaultdict()
        movers['speech'] = "Here are the members of "+sector.name
        card = defaultdict()
        card['title'] = "Members of"+sector.name
        card['companies'] = companies
        movers['text'] = card
        movers['type'] = 'members'
        return movers  


def revenue_reply(company, date_period):
    """
    :param company: A Company whose revenue was requested
    :param date_period: A string containing the date for which revenue data was requested for
    :return: A dictionary containing the layout of the revenue card
    """
    response = {}

    card = {}
    card['title'] = company.name
    card['revenue_data'] = list()

    response['speech'] = "Here is the revenue data for " + company.name
    response['type'] = "revenue"
    response['text'] = card

    valid_date = False

    if not date_period:
        valid_date = True

        for revenue in company.revenue:
            row = {}
            row['date'] = revenue[0]
            row['revenue'] = revenue[1]
            card['revenue_data'].append(row)
    else:
        for revenue in company.revenue:
            if revenue[0][-2:] == date_period[2:4]:
                valid_date = True
                row = {}
                row['date'] = revenue[0]
                row['revenue'] = revenue[1]
                card['revenue_data'].append(row)
                break

    if not valid_date:
        response['speech'] = "I'm sorry, I couldn't find the data you were looking for."
        response['text'] = "I'm sorry, I couldn't find the data you were looking for."
        response['type'] = 'error'

    return response


def daily_briefings(companies, sectors, attributes, days):
    """
    :param companies: A list of Company objects
    :param sectors: A list of Sector objects
    :param attributes: A list of strings that specify the attributes to display data for
    :param days: An integer number of days of news to display
    :return: A dictionary containing the layout of the cards to display
    """
    response = {}

    if not companies and not sectors:
        message = 'You are not currently tracking any companies or sectors. ' \
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
            card = {'name': company.name, 'code': company.code, 'price': company.stock.price, 'date': company.date}
            for attribute in attributes:
                attr = company_attributes[attribute]
                try:
                    value = getattr(company.stock, attr)
                except AttributeError:
                    value = getattr(company, attr)

                if attr == 'news':
                    card[attr] = news_reply(value, days, '')
                else:
                    card[attr] = value
            company_cards.append(card)

        briefing['companies'] = company_cards

        # Get sector news
        sector_attributes = ['highest_price', 'lowest_price', 'rising', 'falling']
        sector_cards = []

        for sector in sectors:
            card = {}

            card['name'] = sector.name

            for attribute in sector_attributes:
                card[attribute] = sector_reply(sector, attribute)

            # Check if user wants sector news
            if 'news' in attributes:
                card['news'] = news_reply(sector.news, days, '')

            sector_cards.append(card)

        briefing['sectors'] = sector_cards

        response['speech'] = 'Here is the latest information I could find!'
        response['text'] = briefing
        response['type'] = 'briefing'

    return response
