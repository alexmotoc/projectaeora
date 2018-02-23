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
