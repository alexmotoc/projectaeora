from __future__ import print_function
from collections import defaultdict
import bs4
import requests
from footsie import Share

#'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1'

def split_string(s, start, end):
    return (s.split(start))[1].split(end)[0].strip()

def scrape_ftse(url):
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

def scrape_company_profiles(url):
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

def scrape_company_sector(url):
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