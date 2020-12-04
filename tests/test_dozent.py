import unittest
from dozent.main import Dozent
from dozent import main
from datetime import date


class DozentTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_days_of_support_defined(self):
        self.assertTrue(type(main.FIRST_DAY_OF_SUPPORT) == date)
        self.assertTrue(type(main.LAST_DAY_OF_SUPPORT) == date)

    def test_dozent_get_date_links(self):
        """
        This test is fairly weak, just checking if the dates
        :return:
        """
        dozent_obj = Dozent()
        len_of_links = len(dozent_obj.get_links_for_days(start_date=main.FIRST_DAY_OF_SUPPORT,
                                                         end_date=main.LAST_DAY_OF_SUPPORT))
        self.assertTrue(len_of_links >= 12 * (2017 - 2020))

    def test_make_date_from_date_link_day_when_is_defined(self):
        date_dict = {
            "day": "03",
            "month": "07",
            "year": "2017",
            "link": "sample-link"
        }

        self.assertTrue(Dozent._make_date_from_date_link(date_dict) == date(year=2017, month=7, day=3))

    def test_make_date_from_date_link_day_when_is_undefined(self):
        date_dict = {
            "day": "NaN",
            "month": "07",
            "year": "2017",
            "link": "sample-link"
        }

        self.assertTrue(Dozent._make_date_from_date_link(date_dict) == date(year=2017, month=7, day=1))


if __name__ == "__main__":
    unittest.main()
