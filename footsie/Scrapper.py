from __future__ import print_function
import bs4
import requests
import json
from footsie import Share

#'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1'

def splitString(s, start, end):
    return (s.split(start))[1].split(end)[0].strip()


def ScrapeWebSite(shares, url,i):
    response = requests.get(url)
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
            diff = splitString(str(data[4]), '">', "<")
            per_diff = data[5].string.strip()
	        #new code below
            fetch_sub_sector = 1
            for s in shares:
                if (s.get_code() == code):
                    s.update_data(current, price, diff, per_diff)
                    fetch_sub_sector = 0
                    break
            if (fetch_sub_sector == 1): 
                #it gets the sector, sub-sector from the company-specific page which is linked in the table
                #probably a better/safer way of doing this, but it works for now
                domain = "http://www.londonstockexchange.com"
                secondURL = domain + (data[6].find('a')['href'])
                sub_sector, sector = ScrapeWebSite2(secondURL, i)
                s = Share.Share(code, name, current, price, diff, per_diff, sub_sector, sector)
                shares.append(s)
                i = i + 1
        return shares, i

#new function to scrape stock-specific page
def ScrapeWebSite2(url, i):
    print("Looking up sector and sub sector ",end='')
    print(i,end='')
    print("/100")
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
        return sub_sector, sector 


'''
Returns the information for a given stock ticker in JSON in the following format:
{
    "code": "III",
    "name": "3I GRP.",
    "currency": "GBX",
    "price": "934.00",
    "difference": "-7.40",
    "percentage_difference": "-0.79",
    "sub_sector": "Specialty Finance",
    "sector": "Financial Services" 
}
TODO: Fill in sub_sector/sector
'''


def returnShareInfoJSON(shares, stock_ticker):
    # Get a JSON string for the entry in shares than contains the stock_ticker

    json_string = ""

    for s in shares:
        if s.get_code() == stock_ticker:
            json_string = json.dumps(s.getDict())
            break

    if json_string:
        return json_string
    else:
        print("Stock doesn't exist")

    # TODO: Throw an error????
