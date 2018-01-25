import json

class Share:


    def __init__(self, code, name, current, price, diff, per_diff):
        self.code = code
        self.name = name
        self.current = current
        self.price = price
        self.diff = diff
        self.per_diff = per_diff
        self.sector = ""
        self.sub_sector = ""
        self.variance = ""
        self.high = ""
        self.low = ""
        self.volume = ""
        self.last_close_value = ""
        self.last_close_date = ""
        self.bid = ""
        self.offer = ""
        self.status = ""
        self.special_condition = ""

    def update(self, price, variance, high, low, volume, last_close_value, last_close_date, bid, offer, status, special_conditions):
        self.price = price
        self.variance = variance
        self.high = high
        self.low = low
        self.volume = volume
        self.last_close_value = last_close_value
        self.last_close_date = last_close_date
        self.bid = bid
        self.offer = offer
        self.status = status
        self.special_conditions = special_conditions

    def print_company_price_data(self): #temporary test function
        print(self.price,end=", ")
        print(self.variance,end=",")
        print(self.high,end=", ")
        print(self.low,end=", ")
        print(self.volume,end=", ")
        print(self.last_close_value,end=", ")
        print(self.last_close_date,end=", ")
        print(self.bid,end=", ")
        print(self.offer,end=", ")
        print(self.status,end=", ")
        print(self.special_conditions.strip())
        print()

    def get_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}'.format(
                self.code, self.name, self.current,
                self.price, self.diff, self.per_diff)
