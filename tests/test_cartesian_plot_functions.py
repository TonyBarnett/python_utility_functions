import unittest
from utility_functions.cartesian_plot_functions import get_r_squared
from math import log10


class RSquared(unittest.TestCase):
    def setUp(self):
        self.x = [1, 2, 3, 4]
        self.log_x = [10, 100, 1000, 10000]
        self.y = [3, 5, 7, 9]
        self.a = 2
        self.b = 1

    def test_simple_case(self):
        r_s = get_r_squared(self.x, self.y, self.a, self.b)
        self.assertEqual(r_s, 1)

    def test_bad_fit(self):
        self.a = 4
        self.b = 2
        r_s = get_r_squared(self.x, self.y, self.a, self.b)
        self.assertAlmostEqual(r_s, -7.2)
