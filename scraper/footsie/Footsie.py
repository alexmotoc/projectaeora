class Footsie:

    def __init__(self, value, diff, per_diff, high, low, prev_close, companies):
        self.value = value
        self.diff = diff
        self.per_diff = per_diff
        self.high = high
        self.low = low
        self.prev_close = prev_close
        self.companies = companies

    def __str__(self):
        return 'Value: {}\nDifference: {}\nPercentage Difference: {}' \
               'High: {}\nLow: {}\nPreviously close: {}\nCompanies: {}\n'.format(
               self.value, self.diff, self.per_diff, self.high,
               self.low, self.prev_close, self.companies)