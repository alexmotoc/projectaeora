import unittest

from footsie import Scraper
from footsie import Sector, Company, News
from datetime import datetime, timedelta

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

    def test_companies_in_empty_sector(self):
        empty_string_list = self.scraper.get_companies_in_sector("")
        self.assertEqual(empty_string_list, [])

    def test_companies_in_non_existent_sector(self):
        abc_string_list = self.scraper.get_companies_in_sector("abc")
        self.assertEqual(abc_string_list, [])

    def test_companies_in_sector(self):
        beverages_sector_list = self.scraper.get_companies_in_sector("Beverages")
        companies_in_beverages = ["DGE", "CCH"]
        self.assertCountEqual(beverages_sector_list, companies_in_beverages)

        insurance_sector_list = self.scraper.get_companies_in_sector("Nonlife Insurance")
        companies_in_insurance = ["DLG", "ADM", "RSA"]
        self.assertCountEqual(insurance_sector_list, companies_in_insurance)

    def test_comapanies_in_empty_sub_sector(self):
        empty_string_list = self.scraper.get_companies_in_sub_sector("")
        self.assertEqual(empty_string_list, [])

    def test_companies_in_non_existent_sub_sector(self):
        abc_string_list = self.scraper.get_companies_in_sub_sector("abc")
        self.assertEqual(abc_string_list, [])

    def test_companies_in_sub_sector(self):
        soft_drinks_sub_sector = self.scraper.get_companies_in_sub_sector("Soft Drinks")
        companies_in_soft_drinks = ["CCH"]
        self.assertCountEqual(soft_drinks_sub_sector, companies_in_soft_drinks)

        specialty_chemicals_sub_sector = self.scraper.get_companies_in_sub_sector("Specialty Chemicals")
        companies_in_specialty_chemicals = ["JMAT", "CRDA"]
        self.assertCountEqual(specialty_chemicals_sub_sector, companies_in_specialty_chemicals)

    # TODO: Make it so that if you're trying to get data on a sector that doesn't exist, return None??
    def test_empty_sector_data(self):
        empty_string_sector = self.scraper.get_sector_data("")
        self.assertIsNone(empty_string_sector)

    def test_non_existent_sector_data(self):
        abc_string_sector = self.scraper.get_sector_data("abc")
        self.assertIsNone(abc_string_sector)

    def test_sector_data(self):
        beverages_sector = self.scraper.get_sector_data("Beverages")
        self.assertIsInstance(beverages_sector, Sector.Sector)
        self.assertEqual(beverages_sector.name, "Beverages")

        beverages_company_list = beverages_sector.companies
        companies_in_beverages = ["CCH", "DGE"]

        self.assertEqual(len(beverages_company_list), 2)

        for company in beverages_company_list:
            self.assertIsInstance(company, Company.Company)
            self.assertIn(company.code, companies_in_beverages)

        insurance_sector = self.scraper.get_sector_data("Nonlife Insurance")
        self.assertIsInstance(insurance_sector, Sector.Sector)
        self.assertEqual(insurance_sector.name, "Nonlife Insurance")

        insurance_company_list = insurance_sector.companies
        companies_in_insurance = ["ADM", "DLG", "RSA"]
        for company in insurance_company_list:
            self.assertIsInstance(company, Company.Company)
            self.assertIn(company.code, companies_in_insurance)

    # TODO: Add tests for when the sector is all lower case etc...

    def test_empty_sub_sector_data(self):
        # TODO: BUG - Error thrown from Scraper when running the line below!
        empty_string_sub_sector = self.scraper.get_sub_sector_data("")
        self.assertIsNone(empty_string_sub_sector)

    def test_non_existent_sub_sector_data(self):
        abc_string_sub_sector = self.scraper.get_sub_sector_data("abc")
        self.assertIsNone(abc_string_sub_sector)

    def test_sub_sector_data(self):
        soft_drinks_sub_sector = self.scraper.get_sub_sector_data("Soft Drinks")
        self.assertIsInstance(soft_drinks_sub_sector, Sector.Sector)
        self.assertEqual(soft_drinks_sub_sector.name, "Soft Drinks")

        soft_drinks_company_list = soft_drinks_sub_sector.companies
        companies_in_soft_drinks = ["CCH"]

        self.assertEqual(len(soft_drinks_company_list), 1)

        for company in soft_drinks_company_list:
            self.assertIsInstance(company, Company.Company)
            self.assertIn(company.code, companies_in_soft_drinks)

        specialty_chemicals_sub_sector = self.scraper.get_sub_sector_data("Specialty Chemicals")
        self.assertIsInstance(specialty_chemicals_sub_sector, Sector.Sector)

        specialty_chemicals_company_list = specialty_chemicals_sub_sector.companies
        companies_in_specialty_chemicals = ["JMAT", "CRDA"]

        for company in specialty_chemicals_company_list:
            self.assertIsInstance(company, Company.Company)
            self.assertIn(company.code, companies_in_specialty_chemicals)

    def test_top5_risers(self):
        top5_risers = self.scraper.get_top5()
        self.assertEqual(len(top5_risers), 5)

        for company in top5_risers:
            self.assertEqual(company[2][0], '+')

    def test_top5_fallers(self):
        top5_fallers = self.scraper.get_top5(risers=False)
        self.assertEqual(len(top5_fallers), 5)

        for company in top5_fallers:
            self.assertEqual(company[2][0], '-')

    #Tests for financial news_stories
    def test_get_financial_news_data(self):
        news = self.scraper.get_financial_news_data('BARC')
        self.assertFalse(len(news) == 0)

        for n in news:
            self.assertIsInstance(n, News.News)
            self.assertIsNotNone(n.date)
            self.assertIsInstance(n.date, str)
            self.assertIsNotNone(n.headline)
            self.assertIsInstance(n.headline, str)
            self.assertIsNotNone(n.url)
            self.assertIsInstance(n.url, str)
            self.assertIsNotNone(n.source)
            self.assertIsInstance(n.source, str)

    def test_get_yahoo_news_data(self):
        yahoo_news = self.scraper.get_yahoo_news_data('BARC')
        self.assertFalse(len(yahoo_news) == 0)

        for n in yahoo_news:
            self.assertIsInstance(n, News.News)
            self.assertIsNotNone(n.date)
            self.assertIsInstance(n.date, str)
            self.assertIsNotNone(n.headline)
            self.assertIsInstance(n.headline, str)
            self.assertIsNotNone(n.url)
            self.assertIsInstance(n.url, str)
            self.assertIsNotNone(n.source)
            self.assertIsInstance(n.source, str)
            self.assertEqual(n.source, 'YAHOO')

    def test_get_financial_news_data_last_x_days(self):
        news_last_3_days = self.scraper.get_financial_news_data_last_x_days('BARC', 3)

        for news_article in news_last_3_days:
            self.assertIsNotNone(news_article.date)
            self.assertIsInstance(news_article.date, str)
            date = datetime.strptime(news_article.date, '%H:%M %d-%b-%Y')
            self.assertIsInstance(news_article, News.News)
            self.assertIsNotNone(news_article.headline)
            self.assertIsInstance(news_article.headline, str)
            self.assertIsNotNone(news_article.url)
            self.assertIsInstance(news_article.url, str)
            self.assertIsNotNone(news_article.source)
            self.assertIsInstance(news_article.source, str)
            self.assertTrue(date.date() >= datetime.now().date() - timedelta(3))

    def test_get_financial_news_data_current_month(self):
        news_current_month = self.scraper.get_financial_news_data_current_month('BARC')

        for news_article in news_current_month:
            self.assertIsNotNone(news_article.date)
            self.assertIsInstance(news_article.date, str)
            date = datetime.strptime(news_article.date, '%H:%M %d-%b-%Y')
            self.assertIsInstance(news_article, News.News)
            self.assertIsNotNone(news_article.headline)
            self.assertIsInstance(news_article.headline, str)
            self.assertIsNotNone(news_article.url)
            self.assertIsInstance(news_article.url, str)
            self.assertIsNotNone(news_article.source)
            self.assertIsInstance(news_article.source, str)
            self.assertTrue(date.date().month == datetime.now().date().month and date.date().year == datetime.now().date().year)

    def test_get_financial_news_data_current_year(self):
        news_current_year = self.scraper.get_financial_news_data_current_year('BARC')
        self.assertFalse(len(news_current_year) == 0)

        for news_article in news_current_year:
            self.assertIsNotNone(news_article.date)
            self.assertIsInstance(news_article.date, str)
            date = datetime.strptime(news_article.date, '%H:%M %d-%b-%Y')
            self.assertIsInstance(news_article, News.News)
            self.assertIsNotNone(news_article.headline)
            self.assertIsInstance(news_article.headline, str)
            self.assertIsNotNone(news_article.url)
            self.assertIsInstance(news_article.url, str)
            self.assertIsNotNone(news_article.source)
            self.assertIsInstance(news_article.source, str)
            self.assertTrue(date.date().year == datetime.now().date().year)

if __name__ == '__main__':
    unittest.main()
