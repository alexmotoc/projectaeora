class News:

    def __init__(self, date, headline, url, source, impact):
        self.date = date
        self.headline = headline
        self.url = url
        self.source = source
        self.impact = impact

    def __str__(self):
        return '{}\nCreated at: {}\nLink: {}\nSource : {}\nImpact: {}'.format(
                self.headline, self.date, self.url, self.source, self.impact)
