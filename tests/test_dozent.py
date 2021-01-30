import unittest
from os.path import exists
from os import walk
from shutil import rmtree

from dozent.dozent import Dozent
from dozent import dozent
from datetime import date


class DozentTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self) -> None:
        if exists("test_downloader_dir"):
            rmtree("test_downloader_dir")

    global dozent_obj

    dozent_obj = Dozent()

    def test_days_of_support_defined(self):
        self.assertTrue(type(dozent.FIRST_DAY_OF_SUPPORT) == date)
        self.assertTrue(type(dozent.LAST_DAY_OF_SUPPORT) == date)

    def test_dozent_get_date_links(self):
        """
        This test is fairly weak, just checking if the dates
        :return:
        """
        len_of_links = len(
            dozent_obj.get_links_for_days(
                start_date=dozent.FIRST_DAY_OF_SUPPORT,
                end_date=dozent.LAST_DAY_OF_SUPPORT,
            )
        )
        self.assertTrue(len_of_links >= 12 * (2017 - 2020))

    def test_make_date_from_date_link_day_when_is_defined(self):
        date_dict = {"day": "03", "month": "07", "year": "2017", "link": "sample-link"}

        self.assertTrue(
            Dozent._make_date_from_date_link(date_dict)
            == date(year=2017, month=7, day=3)
        )

    def test_make_date_from_date_link_day_when_is_undefined(self):
        date_dict = {"day": "NaN", "month": "07", "year": "2017", "link": "sample-link"}

        self.assertTrue(
            Dozent._make_date_from_date_link(date_dict)
            == date(year=2017, month=7, day=1)
        )

    def test_download_test(self):
        dozent_obj.download_test(download_dir="test_downloader_dir", verbose=False)

        _, _, filenames = next(walk("test_downloader_dir"))

        filenames = set(filenames)

        self.assertEqual(
            filenames,
            {"test_500K.txt", "test_650K.txt", "test_600K.txt", "test_550K.txt"},
        )


if __name__ == "__main__":
    unittest.main()
