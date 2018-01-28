class Share:

    def __init__(self, price, diff, per_diff, high, low,
                 volume, last_close_value, last_close_date, bid, offer):
        self.price = price
        self.diff = diff
        self.per_diff = per_diff
        self.high = high
        self.low = low
        self.volume = volume
        self.last_close_value = last_close_value
        self.last_close_date = last_close_date
        self.bid = bid
        self.offer = offer

    def __str__(self):
        return 'Price: {}\nDifference: {}\nPercentage difference: {}\n' \
               'Variance: {}\nHigh: {}\nLow: {}\nVolume: {}\n' \
               'Last close value: {}\nLast close date: {}\nBid: {}\nOffer: {}\n'.format(
               self.price, self.diff, self.per_diff, self.high, self.low,
               self.volume, self.last_close_value, self.last_close_date, self.bid, self.offer)