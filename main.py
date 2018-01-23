import sys

from footsie import Share, Scrapper

shares = list()

print("****************************************SCRAPING FOR NEW DATA****************************************")
lse = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page='

shares = list()
for page in range(1, 7):
    shares += Scrapper.scrape_ftse(lse + str(page))

# Display stock
for share in shares:
    print(share)
