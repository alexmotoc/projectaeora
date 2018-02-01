class Company:

    def __init__(self, code, name, market_cap, revenue,
                 stock, sector, sub_sector, news):
        self.code = code
        self.name = name
        self.market_cap = market_cap
        self.revenue = revenue
        self.stock = stock
        self.sector = sector
        self.sub_sector = sub_sector
        self.news = news

    def __str__(self):
        return 'Code: {}\nName: {}\nMarket cap: {}\nRevenue: {}\n' \
               'Stock: {}\nSector: {}\nSub-sector: {}\nNews: {}\n'.format(
               self.code, self.name, self.market_cap, self.revenue,
               self.stock, self.sector, self.sub_sector, self.news)
