from __future__ import print_function

class Share:
    def __init__(self, code, name, current, price, diff, per_diff, sub_sector, sector):
        self.code = code
        self.name = name
        self.current = current
        self.price = price
        self.diff = diff
        self.per_diff = per_diff
        self.sub_sector = sub_sector
        self.sector = sector

    def update_data(self, current, price, diff, per_diff):
        self.current = current
        self.price = price
        self.diff = diff
        self.per_diff = per_diff
    
    def get_rss_item(self, fe):
        fe.title(self.name)
        fe.id(self.code)
        fe.content(self.code + ',' + self.name + ',' + self.current + ',' + self.price + ',' + self.diff + ',' + self.per_diff)

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name

    def get_sub_sector(self):
        return self.sub_sector

    def get_sector(self):
        return self.sector

    def get_spot_price(self):
        return self.price

    def get_per_diff(self):
        return self.per_diff

    def printAll(self):
        print(self.code, end='')
	print(" , ", end='')
        print(self.name, end='')
	print(" , ", end='')
        print(self.current, end='')
        print(" , ", end='')
        print(self.price, end='')
	print(" , ", end='')
        print(self.diff, end='')
	print(" , ", end='')
        print(self.per_diff, end='')
	print("% , ", end='')
        print(self.sub_sector, end='')
        print(" ,",end='')
        print(self.sector)
