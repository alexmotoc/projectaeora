from collections import defaultdict
import bs4
import json
import requests
import Company, Footsie, News, Share

class Scrapper:

    def __init__(self):
        self.domain = "http://www.londonstockexchange.com"
        self.ftse100URL = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX"
        self.top10URL = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/risers-and-fallers/risers-fallers.html"

        # Get company profiles from local file
        filename = 'data/profiles.json'
        with open(filename, 'r') as f:
            profiles = json.loads(f)
        self.profiles = profiles

    def split_string(self, s, start, end):
        return (s.split(start))[1].split(end)[0].strip()

    def get_ftse(self):
        """Returns a object containing information about FTSE 100 and the companies in this index."""
        # Get general data about FTSE100
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, "lxml")
            table = soup.findAll(attrs={"summary" : "Price data"})[0]
            body = table.find('tbody')
            row = body.find('tr')
            data = r.findAll('td')

            value = data[0].string
            diff = self.split_string(data[1].string)
            per_diff = data[2].string
            high = data[3].string
            low = data[4].string
            prev_close = data[5].string

        # Get data about every company
        companies = list()
        table_url = self.ftse100URL + '&industrySector=&page='
        for i in range(1,7):
            url = table_url + str(i)
            response = requests.get(url)
            if response.status_code == 200:
                soup = bs4.BeautifulSoup(response.content, "lxml")
                table = soup.findAll(attrs={"summary" : "Companies and Prices"})[0]
                body = table.find('tbody')
                rows = body.findAll('tr')

                for r in rows:
                    data = r.findAll('td')
                    code = data[0].string
                    company = get_company_data(code)
                    companies.append(company)

        ftse = Footsie()
        return ftse

    def get_company_profiles(self):
        """Returns a dictionary containing the company codes and the urls associated with their profiles."""
        profiles = dict()
        table_url = self.ftse100URL + '&industrySector=&page='
        for i in range(1,7):
            url = table_url + str(i)
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

        return profiles

    def get_company_data(self, code):
        url = self.domain + self.profiles[code]
        response = requests.get(url)

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, "lxml")
            # Get information about the company
            name = soup.find('div', {'class': 'company-title'}).text
            market_cap = soup.find('td', text='Market cap(in millions)*').string

            revenue = dict()

            revenue_table = soup.findAll(attrs={"summary" : "Fundamentals"})[0]
            head = table.find('thead')
            body = table.find('tbody')
            title = head.find('tr')
            row = body.find('tr')
            dates = title.findAll('td')
            values = row.findAll('td')

            for i in range(1, 6):
                revenue[dates[i]] = values[i]

            sector_tag = soup.find('td', text='FTSE sector')
            sector = sector_tag.findNext('td')
            sub_sector_tag = sector.findNext('td')
            sub_sector = sub_sector_tag.findNext('td')

            # Get stock data
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

            stock = Share(price, variance, high, low, volume,
                          last_close_value, last_close_date, bid, offer)
            news = self.get_financial_news_data(code)

            company = Company(code, name, market_cap, revenue,
                              stock, sector, sub_sector, news)

        return company

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

        :param code: The code of the company for which financial news is wanted.
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

                date = data[0].text.strip()
                headline = data[2].a.text.strip()
                url = data[2].a.get('href')\
                    .replace("javascript: var x=openWin2('", "")\
                    .replace("', 'News', 900, 600, 'resizable=yes,toolbar=no,location=yes,directories=yes,addressbar=yes,scrollbars=yes,status=yes,menubar=no')", "")

                source = data[3].text.strip()
                impact = data[4].text.strip()

                news = News(date, headline, url, source, impact)

                financial_news.append(news)

        return financial_news

    def get_sectors(self):
        """Returns a JSON object containing financial sectors, their corresponding subsectors
        and the companies belonging to each of them."""
        sectors = defaultdict(lambda : defaultdict(list))
        for code, profile in self.profiles.items():
            sector, sub_sector = self.get_company_sector(code)
            sectors[sector][sub_sector].append(code)

        return json.dumps(sectors)
