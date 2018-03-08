from collections import defaultdict
from datetime import datetime

class Sector:

    def __init__(self, name):
        self.name = name
        self.companies = list()
        self.rising = list()
        self.falling = list()
        self.news = defaultdict(list)
        self.highest_price = None
        self.lowest_price = None
        self.performing = list()

    def add_company(self, company):
        self.companies.append(company)

        if "+" in company.stock.per_diff:
            self.rising.append(company)
            self.rising.sort(key=lambda x: float(x.stock.per_diff[1:]), reverse=True)
        else:
            self.falling.append(company)
            self.falling.sort(key=lambda x: float(x.stock.per_diff[1:]), reverse=True)

        self.performing = self.rising + self.falling[::-1]

        self.news['LSE'] += company.news['LSE']
        self.news['YAHOO'] += company.news['YAHOO']

        if self.highest_price == None:
            self.highest_price = company
        else:
            if float(company.stock.price.replace(",","")) > float(self.highest_price.stock.price.replace(",","")):
                self.highest_price = company

        if self.lowest_price == None:
            self.lowest_price = company
        else:
            if float(company.stock.price.replace(",","")) < float(self.lowest_price.stock.price.replace(",","")):
                self.lowest_price = company
