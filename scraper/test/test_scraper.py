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

    # TODO: Make it so that if a given sector is empty, return None - the current implementation for get_companies_in_sub_sector(..) does this.
    def test_non_existent_sector(self):
        empty_string_list = self.scraper.get_companies_in_sector("")
        self.assertEqual(empty_string_list, None)

        abc_string_list = self.scraper.get_companies_in_sector("abc")
        self.assertEqual(abc_string_list, None)

    def test_companies_in_sector(self):
        beverages_sector_list = self.scraper.get_companies_in_sector("Beverages")
        companies_in_beverages = ["CCH", "DGE"]
        self.assertCountEqual(beverages_sector_list, companies_in_beverages)

        insurance_sector_list = self.scraper.get_companies_in_sector("Nonlife Insurance")
        companies_in_insurance = ["ADM", "DLG", "RSA"]
        self.assertCountEqual(insurance_sector_list, companies_in_insurance)

    def test_non_existent_sub_sector(self):
        empty_string_list = self.scraper.get_companies_in_sub_sector("")
        self.assertEqual(empty_string_list, None)

        abc_string_list = self.scraper.get_companies_in_sub_sector("abc")
        self.assertEqual(abc_string_list, None)

    def test_companies_in_sub_sector(self):
        soft_drinks_sub_sector = self.scraper.get_companies_in_sub_sector("Soft Drinks")
        companies_in_soft_drinks = ["CCH"]
        self.assertCountEqual(soft_drinks_sub_sector, companies_in_soft_drinks)

        specialty_chemicals_sub_sector = self.scraper.get_companies_in_sub_sector("Specialty Chemicals")
        companies_in_specialty_chemicals = ["JMAT", "CRDA"]
        self.assertCountEqual(specialty_chemicals_sub_sector, companies_in_specialty_chemicals)


if __name__ == '__main__':
    unittest.main()