import unittest
from utility_functions.range_operators import float_range


class FloatRange(unittest.TestCase):
    def test_type(self):
        x = float_range(1, 2, 0.1)
        self.assertIs(type(x), list)

    def test_simple_case(self):
        x = float_range(1, 2, 0.1)
        output = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
        self.assertEqual(len(x), len(output))
        for i, x_i in enumerate(x):
            self.assertAlmostEqual(x_i, output[i])

    def test_start_only(self):
        x = float_range(2, step=0.1)
        output = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
        self.assertEqual(len(x), len(output))
        for i, x_i in enumerate(x):
            self.assertAlmostEqual(x_i, output[i])