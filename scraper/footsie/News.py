class News:

    def __init__(self, date, headline, url, source, impact, description, company):
        self.date = date
        self.headline = headline
        self.url = url
        self.source = source
        self.impact = impact
        self.description = description
        self.company = company

    def __str__(self):
        return '{}\nCreated at: {}\nLink: {}\nSource : {}\nImpact: {}'.format(
                self.headline, self.date, self.url, self.source, self.impact)

