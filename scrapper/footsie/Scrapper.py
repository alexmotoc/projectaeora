from collections import defaultdict
import bs4
import json
import os
import requests
from footsie import Company, Footsie, News, Share, Sector
from datetime import datetime, timedelta

class Scrapper:

    def __init__(self):
        self.domain = "http://www.londonstockexchange.com"
        self.ftse100URL = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX"
        self.top5URL = "http://www.londonstockexchange.com/media/iframe/fallers.htm"
        self.ftse100_summary = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices.html?index=UKX"
        # Get company profiles from local file
        filename = os.path.dirname(__file__) + '/../data/profiles.json'
        with open(filename, 'r') as f:
            profiles = json.load(f)
        self.profiles = profiles
        #Get sectors from local file
        filename = os.path.dirname(__file__) + '/../data/sectors.json'
        sectors = defaultdict(lambda : defaultdict(set))
        with open(filename, 'r') as f:
            sectors = json.load(f)
        self.sectors = sectors

    def get_companies_in_sector(self, requested_sector): 
        #returns list of codes of companies in the requested_sector
        companies_in_sector = list()
        for sector, sub_sectors in self.sectors.items():
            if sector == requested_sector:
                for sub_sector, companies in sub_sectors.items():
                    for company in companies:
                        companies_in_sector.append(company)
                break
        return companies_in_sector

    def get_companies_in_sub_sector(self, requested_sub_sector): 
        #returns list of codes of companies in the requested_sub_sector
        companies_in_sub_sector = list()
        for sector, sub_sectors in self.sectors.items():
            for sub_sector, companies in sub_sectors.items():
                if sub_sector == requested_sub_sector:
                    for company in companies:
                        companies_in_sub_sector.append(company)
                    return companies_in_sub_sector

    def get_sector_data(self, sector_name):
        #Returns a Sector object
        sector = Sector.Sector(sector_name)
        companies = self.get_companies_in_sector(sector_name)    
        for company in companies:
            sector.add_company(self.get_company_data(company))
        return sector

    def get_sub_sector_data(self, sub_sector_name):
        #Returns a Sector object
        sub_sector = Sector.Sector(sub_sector_name)
        companies = self.get_companies_in_sub_sector(sub_sector_name)     
        for company in companies:
            sub_sector.add_company(self.get_company_data(company))
        return sub_sector

    def split_string(self, s, start, end):
        return (s.split(start))[1].split(end)[0].strip()

    def get_ftse(self):
        """Returns a object containing information about FTSE 100 and the companies in this index."""
        # Get general data about FTSE100
        response = requests.get(self.ftse100_summary)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, "lxml")
            table = soup.findAll(attrs={"summary" : "Price data"})[0]
            body = table.find('tbody')
            row = body.find('tr')
            data = row.findAll('td')

            value = data[0].string
            diff = self.split_string(str(data[1]), '">', "<")
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
                    company = self.get_company_data(code)
                    companies.append(company)

        ftse = Footsie.Footsie(value, diff, per_diff, high, low, prev_close, companies)
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
                    profile = data[1].find('a')['href']
                    profiles[code] = profile

        return profiles

    def get_company_data(self, code):
        url = self.domain + self.profiles[code]
        response = requests.get(url)

        company = None
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, "lxml")
            # Get information about the company
            name_cell = soup.find('div', {'class': 'company-title'})
            name = name_cell.text.strip().split('\r')[1].strip()
            market_cap = soup.find('td', text='Market cap(in millions)*').findNext('td').string

            revenue = dict()

            revenue_table = soup.findAll(attrs={"summary" : "Fundamentals"})[0]
            head = revenue_table.find('thead')
            body = revenue_table.find('tbody')
            title = head.find('tr')
            row = body.find('tr')
            dates = title.findAll('th')
            values = row.findAll('td')

            for i in range(1, len(dates)):
                revenue[dates[i].string.strip()] = values[i].string.strip()

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

            # Process variance cell
            per_diff = variance.text[:variance.text.find('%')]
            diff = variance.text[variance.text.find('%') + 1:]

            stock = Share.Share(price.string, diff, per_diff, high.string,
                                low.string, volume.string, last_close_value,
                                last_close_date, bid.string, offer.string)
            news = self.get_financial_news_data(code)

            company = Company.Company(code, name, market_cap, revenue,
                              stock, sector.string, sub_sector.string, news)

        return company

    def get_top5(self, risers=True):
        """
        Returns a list containing the codes of the top 10 companies.

        Keyword arguments:
        url - the url of the company website to be scrapped
        risers - specified whether to get the risers (True) or fallers (False)
        """
        if risers:
            url = self.top5URL.replace("fallers", "risers")
        else:
            url = self.top5URL
        response = requests.get(url)
        top5 = ""
        if(response.status_code == 200):
            soup = bs4.BeautifulSoup(response.content, "lxml")
            table = soup.findAll(attrs={"summary" : "Companies and Prices"})[0]
            body = table.find('tbody')
            rows = body.findAll('tr')
            i = 1
            for r in rows:
                name = r.find('td').find('a').string
                price = r.findAll('td')[2].string  
                per_diff = self.split_string(str(r.findAll('td')[4]), '">', "<")
                top5 += (name+"\t"+price+"\t"+per_diff)
                if i < 5: 
                    top5 += "\n"
                i = i + 1
        return top5


    def get_financial_news_data(self, code):
        """

        :param code: The code of the company for which financial news is wanted.
        :return: A list containing dictionaries for each piece of most recent news.
        """
        url = self.domain + self.profiles[code]
        url = url.replace("summary/company-summary/", "exchange-insight/news-analysis.html?fourWayKey=")
        # Remove .html from the end
        url = url[:-5]
        # http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/summary/company-summary/GB0031348658GBGBXSET1.html
        # http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/exchange-insight/news-analysis.html?fourWayKey=GB0031348658GBGBXSET1

        response = requests.get(url)
        financial_news = list()

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, "lxml")
            try:
                table = soup.findAll(attrs={"summary": "table: News Impact"})[0]
            except IndexError:
                return financial_news
            body = table.find('tbody')
            rows = body.findAll('tr')

            for r in rows:
                data = r.findAll('td')

                date = data[0].text.strip()
                headline = data[2].a.text.strip()
                url = self.domain + data[2].a.get('href')\
                    .replace("javascript: var x=openWin2('", "")\
                    .replace("', 'News', 900, 600, 'resizable=yes,toolbar=no,location=yes,directories=yes,addressbar=yes,scrollbars=yes,status=yes,menubar=no')", "")

                source = data[3].text.strip()
                impact = data[4].text.strip()

                news = News.News(date, headline, url, source, impact)

                financial_news.append(news)

        return financial_news

    def get_yahoo_news_data(self, code): 
        """can use this to complement LSE news
        if we're gonna use this, we could extend News.py to store a description
        would also be trivial to create a get_yahoo_news_data_current_month() etc -> only one line would be different from LSE versions"""
        #https://developer.yahoo.com/finance/company.html
        yahoo_news = list()
        url = "http://finance.yahoo.com/rss/headline?s=" + code.split('.')[0] + ".L" 
        response = requests.get(url)
        if (response.status_code == 200):
            soup = bs4.BeautifulSoup(response.content, "xml")
            items = soup.findAll('item')
            for item in items:
                headline = item.title.text
                description = item.description.text 
                date = item.pubDate.text
                date = date.split('+')[0] #remove timezone section of string
                date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S ')
                date = date.strftime('%H:%M %d-%b-%Y') #convert to same format as LSE dates
                url = item.link.text
                source = "YAHOO"
                impact = "N/A"
                news = News.News(str(date), headline, url, source, impact)
                yahoo_news.append(news)
        return yahoo_news
    
    def get_financial_news_data_last_x_days(self, code, x):
        news_stories = self.get_financial_news_data(code)
        news_stories_last_x_days = list()
        for n in news_stories:
            date = datetime.strptime(n.date, '%H:%M %d-%b-%Y')
            if (date.date() >= datetime.now().date() - timedelta(x)):
                news_stories_last_x_days.append(n)
        return news_stories_last_x_days

    def get_financial_news_data_current_month(self, code):
        news_stories = self.get_financial_news_data(code)
        news_stories_current_month = list()
        for n in news_stories:
            date = datetime.strptime(n.date, '%H:%M %d-%b-%Y')
            if (date.date().month == datetime.now().date().month and date.date().year == datetime.now().date().year):
                news_stories_current_month.append(n)
        return news_stories_current_month

    def get_financial_news_data_current_year(self, code):
        news_stories = self.get_financial_news_data(code)
        news_stories_current_year = list()
        for n in news_stories:
            date = datetime.strptime(n.date, '%H:%M %d-%b-%Y')
            if (date.date().year == datetime.now().date().year):
                news_stories_current_year.append(n)
        return news_stories_current_year 
    
    def get_sectors(self):
        """Returns a JSON object containing financial sectors, their corresponding subsectors
        and the companies belonging to each of them."""
        sectors = defaultdict(lambda : defaultdict(list))
        for code, profile in self.profiles.items():
            company = self.get_company_data(code)
            sector = company.sector
            sub_sector = company.sub_sector
            sectors[sector][sub_sector].append(code)

        return json.dumps(sectors)
