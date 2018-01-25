from collections import defaultdict
import bs4
import json
import requests
from footsie import Share

#'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1'


class Scrapper:

    def __init__(self, shares, profiles):
        self.shares = shares
        self.profiles = profiles
        self.domain = "http://www.londonstockexchange.com"
        self.ftse100URL = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page="
        self.top10URL = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/risers-and-fallers/risers-fallers.html"
        if len(shares) == 0:
            self.shares = self.get_ftse()
        if len(profiles) == 0:
            self.profiles = self.get_company_profiles()


    def split_string(self, s, start, end):
        return (s.split(start))[1].split(end)[0].strip()

    def get_ftse(self):
        """
        Returns a list of shares information.

        Keyword arguments:
        url -- the url of the website to be scrapped
        """
        shares = list()
        for i in range(1,7):
            url = self.ftse100URL + str(i)
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
                    diff = self.split_string(str(data[4]), '">', "<")
                    per_diff = data[5].string.strip()
                    s = Share.Share(code, name, current, price, diff, per_diff)
                    shares.append(s)
        self.shares = shares
        return self.shares

    def get_company_profiles(self):
        """
        Returns a dictionary containing the company codes and the urls associated with their profiles.

        Keyword arguments:
        url -- the url of the website to be scrapped
        """
        profiles = dict()
        for i in range(1,7):
            url = self.ftse100URL + str(i)
            response = requests.get(url)

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
        self.profiles = profiles
        return self.profiles

    def get_company_sector(self, code):
        """
        Returns the sector and the sub-sector to which a particular company belongs to.

        Keyword arguments:
        url - the url of the company website to be scrapped
        """
        for s in self.shares:
            if s.code == code and len(s.sector)>0:
                return s.sector, s.sub_sector
            elif s.code == code:
                break
        url = self.domain + self.profiles[code]
        response = requests.get(url)

        if (response.status_code == 200):
            soup = bs4.BeautifulSoup(response.content, "lxml")
            sector_tag = soup.find('td', text='FTSE sector')
            sector = sector_tag.findNext('td')
            sub_sector_tag = sector.findNext('td')
            sub_sector = sub_sector_tag.findNext('td')
            s.sector = sector.string
            s.sub_sector = sub_sector.string
        return sector.string, sub_sector.string

    def scrape_company_price_data(self, code):
        #unfinished
        url = self.domain + self.profiles[code]
        url = url.replace("company-summary-chart.html?fourWayKey=", "company-summary/")
        url = url + ".html"
        response = requests.get(url)
        if(response.status_code == 200):
            #obtains price, variance, high, low, volume, last_close, bid, offer, status and special condition from profile summary page table
            soup = bs4.BeautifulSoup(response.content, "lxml")
            variance_tag = soup.find('td', text='Var % (+/-)')
            price = variance_tag.findPrevious('td')
            variance = variance_tag.findNext('td').findNext('span')
            high_tag = variance.findNext('td')
            high = high_tag.findNext('td')
            low_tag = high.findNext('td')
            low = low_tag.findNext('td')
            volume_tag = low.findNext('td')
            volume = volume_tag.findNext('td')
            last_close_tag = volume.findNext('td')
            last_close = last_close_tag.findNext('td')
            last_close_value = last_close.string.split()[0]
            last_close_date = last_close.string.split()[2]
            bid_tag = last_close.findNext('td')
            bid = bid_tag.findNext('td')
            offer_tag = bid.findNext('td')
            offer = offer_tag.findNext('td')
            status_tag = offer.findNext('td')
            status = status_tag.findNext('td')
            special_conditions_tag = status.findNext('td')
            special_conditions = special_conditions_tag.findNext('td')
        #need to update Share.py to cater for new variables and get rid of ugly return
        for s in self.shares:
            if s.code == code:
                s.update(price.string, variance.string, high.string, low.string, volume.string, last_close_value, last_close_date, bid.string, offer.string, status.string, special_conditions.string)
                break
        return s
        

    def get_top10(self, risers=True):
        """
        Returns a list containing the codes of the top 10 companies.

        Keyword arguments:
        url - the url of the company website to be scrapped
        risers - specified whether to get the risers (True) or fallers (False)
        """
        response = requests.get(self.top10URL)
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


    def get_financial_news_data(self, code):
        """

        :param url: The url of the company for which financial news is wanted.
        :return: A list containing dictionaries for each piece of most recent news.
        """
        url = self.domain + self.profiles[code]
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


    def get_sectors(self):
        """
        Returns a JSON object containing financial sectors, their corresponding subsectors
        and the companies belonging to each of them.

        Keyword arguments:
        profiles - a dictionary containing company codes and their associated profile urls
        """
        profiles = self.profiles
        domain = "http://www.londonstockexchange.com"
        sectors = defaultdict(lambda : defaultdict(list))
        for code, profile in profiles.items():
            sector, sub_sector = self.get_company_sector(code)
            sectors[sector][sub_sector].append(code)

        return json.dumps(sectors)
