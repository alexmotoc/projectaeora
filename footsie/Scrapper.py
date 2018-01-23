from __future__ import print_function
import bs4
import requests
from footsie import Share

#'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1'

def split_string(s, start, end):
    return (s.split(start))[1].split(end)[0].strip()

def scrape_ftse(url):
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

            # Get specific information about the company (e.g. sector)
            domain = "http://www.londonstockexchange.com"
            secondURL = domain + (data[6].find('a')['href'])
            sector, sub_sector = scrape_stock(secondURL)
            s = Share.Share(code, name, current, price, diff, per_diff, sector, sub_sector)
            shares.append(s)

    return shares

def scrape_stock(url):
    response = requests.get(url)

    if (response.status_code == 200):
        soup = bs4.BeautifulSoup(response.content, "lxml")
        table = soup.findAll(attrs={"summary" : "Trading Information"})[0]
        body = table.find('tbody')
        rows = body.findAll('tr')

        for r in rows:
            data = r.findAll('td')
            if (data[0].string == 'FTSE sub-sector'):
                sub_sector = data[1].string
            elif (data[0].string == 'FTSE sector'):
                sector = data[1].string

    return sector, sub_sector

