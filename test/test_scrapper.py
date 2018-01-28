import unittest
from footsie import Scrapper

class TestScrapper(unittest.TestCase):

    def setUp(self):
        self.scrapper = Scrapper.Scrapper()
        self.company = self.scrapper.get_company_data('BARC')

    def test_company_name(self):
        self.assertTrue(self.company.name, 'BARCLAYS PLC ORD 25P')

    def test_company_sectors(self):
        self.assertTrue(self.company.sector, 'Banks')
        self.assertTrue(self.company.sub_sector, 'Banks')

    def test_revenue(self):
        self.assertTrue(self.company.revenue['31-Dec-12'], 34625.00)
        self.assertTrue(self.company.revenue['31-Dec-13'], 36883.00)
        self.assertTrue(self.company.revenue['31-Dec-14'], 32278.00)
        self.assertTrue(self.company.revenue['31-Dec-15'], 31803.00)
        self.assertTrue(self.company.revenue['31-Dec-16'], 27747.00)

if __name__ == '__main__':
    unittest.main()