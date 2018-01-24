import json
import sys

from collections import defaultdict
from footsie import Share, Scrapper

def get_sectors(profiles):
    """
    Returns a JSON object containing financial sectors, their corresponding subsectors
    and the companies belonging to each of them.

    Keyword arguments:
    profiles - a dictionary containing company codes and their associated profile urls
    """
    domain = "http://www.londonstockexchange.com"
    sectors = defaultdict(lambda : defaultdict(list))
    for code, profile in profiles.items():
        sector, sub_sector = Scrapper.scrape_company_sector(domain + profile)
        sectors[sector][sub_sector].append(code)

    return json.dumps(sectors)

print("****************************************SCRAPING FOR NEW DATA****************************************")
lse = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page='

shares = list()
profiles = dict()
for page in range(1, 7):
    # shares += Scrapper.scrape_ftse(lse + str(page))
    profiles.update(Scrapper.scrape_company_profiles(lse + str(page)))