from datetime import datetime

class Sector:

    def __init__(self, name):
        self.name = name
        self.companies = list()
        self.risers = list()
        self.fallers = list()
        self.news = list()
        self.highest_price = None
        self.lowest_price = None

    def add_company(self, company):
        self.companies.append(company)
        if "+" in company.stock.per_diff:
            self.risers.append(company)
            self.risers.sort(key=lambda x: x.stock.per_diff, reverse=True)
        else:
            self.fallers.append(company)
            self.fallers.sort(key=lambda x: x.stock.per_diff, reverse=True)
        for n in company.news:
            self.news.append(n)
        self.news.sort(key=lambda x: datetime.strptime(x.date, '%H:%M %d-%b-%Y'), reverse=True) #latest article first
        if self.highest_price == None:
            self.highest_price = company
        else:
            if company.stock.price > self.highest_price.stock.price:
                self.highest_price = company
        if self.lowest_price == None:
            self.lowest_price = company
        else:
            if company.stock.price < self.lowest_price.stock.price:
                self.lowest_price = company
