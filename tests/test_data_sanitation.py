import unittest

from utility_functions.data_sanitation import clean_value, _is_top_level_char


class TestCleanValue(unittest.TestCase):
    # TODO make tests to check for UNFCCC badness
    def test_range(self):
        test_case = clean_value("SIC4", "14.49-53")
        self.assertListEqual(test_case, ["14_49", "14_50", "14_51", "14_52", "14_53"])

    def test_smaller_range(self):
        test_case = clean_value("SIC4", "10.08-11")
        self.assertListEqual(test_case, ["10_08", "10_09", "10_10", "10_11"])

    def test_remove_other(self):
        test_case = clean_value("SIC4", "23OTHER")
        self.assertListEqual(test_case, ["23"])

    def test_not_(self):
        test_case = clean_value("SIC4", "23.4 not 23.47")
        self.assertListEqual(test_case,
                             ["23_4"]
                             )

    def test_and_(self):
        test_cast = clean_value("SIC4", "1 & 2")
        self.assertListEqual(test_cast, ["1", "2"])

    def test_strip_slash(self):
        test_case = clean_value("SIC4", "23.12/4")
        self.assertListEqual(test_case, ["23_12"])

    def test_leading_chars(self):
        test_case = clean_value("SITC4", "A05-A10")
        self.assertListEqual(test_case, ["05", "06", "07", "08", "09", "10"])

    def test_bad_range(self):
        with self.assertRaises(Exception):
            clean_value("SIC4", "12.5-1")

    def test_none(self):
        with self.assertRaises(Exception):
            clean_value("SIC", None)

    def test_top_level_char(self):
        test_case = clean_value("SIC4", "B")
        self.assertListEqual(test_case, ["B"])

    def test_with_cpa(self):
        test_case = clean_value("SIC4", "CPA_02")
        self.assertListEqual(test_case, ["02"])


class TestIsTopLevelChar(unittest.TestCase):
    def test_simple_case(self):
        self.assertTrue(_is_top_level_char("A"))

    def test_numeric(self):
        self.assertFalse(_is_top_level_char("1"))

    def test_alphanum(self):
        self.assertFalse(_is_top_level_char("a2"))

    def test_multiple_chars(self):
        self.assertFalse(_is_top_level_char("BE"))

    def test_leading_space(self):
        self.assertFalse(_is_top_level_char(" B"))

    def test_trailing_space(self):
        self.assertFalse(_is_top_level_char("B "))

    def test_lower_case(self):
        self.assertTrue(_is_top_level_char("f"))
