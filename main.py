import json
import sys

from collections import defaultdict
from footsie import Share, Scrapper

shares = list()
profiles = dict()

#could read in saved data files for saved shares, profiles data, and use those

web_scraper_interface = Scrapper.Scrapper(shares, profiles)
shares = web_scraper_interface.get_ftse()
profiles = web_scraper_interface.get_company_profiles()

#save shares,profiles to file


"""tests...
print("JSON...") 
print(web_scraper_interface.get_sectors()) #this bit takes a while since we haven't stored sectors yet
print("TOP 10")
top10 = web_scraper_interface.get_top10(True)
for item in top10:
    print(item)
print()
print("JSON again...") 
print(web_scraper_interface.get_sectors()) #uses stored data this time
print()
print("Share sector, sub-sector, and current price data...")
for s in shares:
    print(s.code,end=", sector=")
    sector, sub_sector = web_scraper_interface.get_company_sector(s.code)
    print(sector,end=", sub_sector=")
    print(sub_sector)
    print("Company Price Data: ", end="")
    s = web_scraper_interface.scrape_company_price_data(s.code)
    s.print_company_price_data()
print("NEWS for a few companies")
i = 0
for s in shares:
    if i%9 == 2:
        news = web_scraper_interface.get_financial_news_data(s.code)
        for n in news:
            print(n)
    i = i + 1
"""
