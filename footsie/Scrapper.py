from __future__ import print_function
from collections import defaultdict
import bs4
import json
import requests
from footsie import Share

#'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1'

def split_string(s, start, end):
    return (s.split(start))[1].split(end)[0].strip()

def get_ftse(url):
    """
    Returns a list of shares information.

    Keyword arguments:
    url -- the url of the website to be scrapped
    """
    response = requests.get(url)
    shares = list()

    if(response.status_code == 200):
        soup = bs4.BeautifulSoup(response.content, "lxml")
        table = soup.findAll(attrs={"summary" : "Companies and Prices"})[0]
        body = table.find('tbody')
        rows = body.findAll('tr')

        for r in rows:
            data = r.findAll('td')
            code = data[0].string
            name = data[1].findChildren()[0].string
            current = data[2].string
            price = data[3].string
            diff = split_string(str(data[4]), '">', "<")
            per_diff = data[5].string.strip()
            s = Share.Share(code, name, current, price, diff, per_diff)
            shares.append(s)

    return shares

def get_company_profiles(url):
    """
    Returns a dictionary containing the company codes and the urls associated with their profiles.

    Keyword arguments:
    url -- the url of the website to be scrapped
    """
    response = requests.get(url)
    profiles = dict()

    if(response.status_code == 200):
        soup = bs4.BeautifulSoup(response.content, "lxml")
        table = soup.findAll(attrs={"summary" : "Companies and Prices"})[0]
        body = table.find('tbody')
        rows = body.findAll('tr')

        for r in rows:
            data = r.findAll('td')
            code = data[0].string
            profile = data[6].find('a')['href']
            profiles[code] = profile

    return profiles

def get_company_sector(url):
    """
    Returns the sector and the sub-sector to which a particular company belongs to.

    Keyword arguments:
    url - the url of the company website to be scrapped
    """
    response = requests.get(url)

    if (response.status_code == 200):
        soup = bs4.BeautifulSoup(response.content, "lxml")
        sector_tag = soup.find('td', text='FTSE sector')
        sector = sector_tag.findNext('td')
        sub_sector_tag = sector.findNext('td')
        sub_sector = sub_sector_tag.findNext('td')

    return sector.string, sub_sector.string

def get_company_price_data(url):
    #unfinished - see variance data, and method of return
    url = url.replace("company-summary-chart.html?fourWayKey=", "company-summary/")
    url = url + ".html"
    response = requests.get(url)
    if(response.status_code == 200):
        #obtains price, variance, high, low, volume, last_close, bid, offer, status and special condition from profile summary page table
        soup = bs4.BeautifulSoup(response.content, "lxml")
        variance_tag = soup.find('td', text='Var % (+/-)')
        price = variance_tag.findPrevious('td')
        variance_tag = soup.find('td', text='Var % (+/-)')
        variance = variance_tag.findNext('td') #the td isn't just plaintext, need to process this cell further
        high_tag = variance.findNext('td')
        high = high_tag.findNext('td')
        low_tag = high.findNext('td')
        low = low_tag.findNext('td')
        volume_tag = low.findNext('td')
        volume = volume_tag.findNext('td')
        last_close_tag = volume.findNext('td')
        last_close = last_close_tag.findNext('td')
        bid_tag = last_close.findNext('td')
        bid = bid_tag.findNext('td')
        offer_tag = bid.findNext('td')
        offer = offer_tag.findNext('td')
        status_tag = offer.findNext('td')
        status = status_tag.findNext('td')
        special_conditions_tag = status.findNext('td')
        special_conditions = special_conditions_tag.findNext('td')
    #better to return values in a structure instead
    return price.string, variance.string, high.string, low.string, volume.string, last_close.string, bid.string, offer.string, status.string, special_conditions.string

def get_top10(url, risers=True):
    """
    Returns a list containing the codes of the top 10 companies.

    Keyword arguments:
    url - the url of the company website to be scrapped
    risers - specified whether to get the risers (True) or fallers (False)
    """
    response = requests.get(url)
    top10 = list()
    index = 0 if risers else 1

    if(response.status_code == 200):
        soup = bs4.BeautifulSoup(response.content, "lxml")
        table = soup.findAll(attrs={"summary" : "Companies and Prices"})[index]
        body = table.find('tbody')
        rows = body.findAll('tr')

        for r in rows:
            data = r.find('td')
            top10.append(data.string)

    return top10


def get_financial_news_data(url):
    """

    :param url: The url of the company for which financial news is wanted.
    :return: A list containing dictionaries for each piece of most recent news.
    """
    url = url.replace("summary/company-summary-chart", "exchange-insight/news-analysis")
    # http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/summary/company-summary-chart.html?fourWayKey=GB00B01FLG62GBGBXSET1
    # http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/exchange-insight/news-analysis.html?fourWayKey=GB00B01FLG62GBGBXSET1

    response = requests.get(url)
    financial_news = list()

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.content, "lxml")
        table = soup.findAll(attrs={"summary": "table: News Impact"})[0]
        body = table.find('tbody')
        rows = body.findAll('tr')

        for r in rows:
            data = r.findAll('td')

            row_data = {}

            row_data["time_and_date"] = data[0].text.strip()
            row_data["code"] = data[1].text.strip()
            row_data["headline"] = data[2].a.text.strip()
            row_data["headline_url"] = data[2].a\
                .get('href')\
                .replace("javascript: var x=openWin2('", "")\
                .replace("', 'News', 900, 600, 'resizable=yes,toolbar=no,location=yes,directories=yes,addressbar=yes,scrollbars=yes,status=yes,menubar=no')", "")

            row_data["source"] = data[3].text.strip()
            row_data["impact"] = data[4].text.strip()

            row_data["impact_img_url"] = data[4].img.get('src')

            financial_news.append(row_data)

    return financial_news
