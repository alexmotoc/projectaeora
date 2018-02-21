import unittest
from footsie import Scraper

class TestScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper.Scraper()
        self.company = self.scraper.get_company_data('BARC')

    def test_company_name(self):
        self.assertEqual(self.company.name, 'BARCLAYS PLC')

    def test_empty_company_code(self):
        self.assertEqual(self.scraper.get_company_data(''), None)

    def test_non_existent_company_code(self):
        self.assertEqual(self.scraper.get_company_data('JDFAKL'), None)

    def test_company_sectors(self):
        self.assertEqual(self.company.sector, 'Banks')
        self.assertEqual(self.company.sub_sector, 'Banks')

    def test_revenue(self):
        self.assertEqual(self.company.revenue['31-Dec-12'], '34625.00')
        self.assertEqual(self.company.revenue['31-Dec-13'], '36883.00')
        self.assertEqual(self.company.revenue['31-Dec-14'], '32278.00')
        self.assertEqual(self.company.revenue['31-Dec-15'], '31803.00')
        self.assertEqual(self.company.revenue['31-Dec-16'], '27747.00')

if __name__ == '__main__':
    unittest.main()