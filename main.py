import tornado.web
import sys

from footsie import Share, Scrapper
import sectorJSON

shares = list()
sub_sectors = list()
sectors = list()
for x in range (0,10000): #just to make testing easier
    print("****************************************SCRAPING FOR NEW DATA****************************************")
    shares, i = Scrapper.ScrapeWebSite(shares,'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1', 0)
    shares, i = Scrapper.ScrapeWebSite(shares,'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=2', i)    
    shares, i = Scrapper.ScrapeWebSite(shares,'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=3', i)
    shares, i = Scrapper.ScrapeWebSite(shares,'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=4', i)
    shares, i = Scrapper.ScrapeWebSite(shares,'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=5', i)
    shares, i = Scrapper.ScrapeWebSite(shares,'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=6', i)
    if (x == 0):
        for s in shares:
        #fe = fg.add_entry()

            s.printAll()       
            sub_sector = s.get_sub_sector()
            if (sub_sector not in sub_sectors):
                sub_sectors.append(sub_sector)
            sector = s.get_sector()
            if (sector not in sectors):
                sectors.append(sector) 
    if (x >= 1):
        # Uncomment below to test the json for each stock
        # stock_choice = input("Pick a stock to get info about: ")
        # for s in shares:
        #     if s.get_code() == stock_choice:
        #         print(s.returnJSON())

        # # Uncomment below to test the json for each sector
        # sector_choice = input("Pick a sector to get info about: ")
        # print(sectorJSON.returnSectorJSON(shares, sector_choice))

        # # Uncomment below to test the json for each sector
        # sub_sector_choice = input("Pick a sub-sector to get info about: ")
        # print(sectorJSON.returnSubSectorJSON(shares, sub_sector_choice))

        i = 0
        for sector in sectors:
            print("Option ",end='')
            print(i, end='')
            print(": ",end='')
            print(sector)
            i = i + 1
        choice = input("Which category?: ")
        for s in shares:
            if (s.get_sector() == sectors[choice]):
                s.printAll()
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
        for s in shares:
            s.printAll()
