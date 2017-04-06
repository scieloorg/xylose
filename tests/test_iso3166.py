import unittest

from xylose import iso3166


class ISO3166Tests(unittest.TestCase):

    def test_load_alpha_2(self):

        data = iso3166.load_alpha_2()

        self.assertEqual(data['BR']['name'],  'Brazil')

    def test_load_alpha_3(self):

        data = iso3166.load_alpha_3()

        self.assertEqual(data['BRA']['name'],  'Brazil')

    def test_load_alpha_2_forms(self):

        data = iso3166.load_alpha_2_forms()

        self.assertEqual(data['brazil'],  'BR')
        self.assertEqual(data['brasil'],  'BR')
        self.assertEqual(data['br'],  'BR')
        self.assertEqual(data['bra'],  'BR')

    def test_load_alpha_3_forms(self):

        data = iso3166.load_alpha_3_forms()

        self.assertEqual(data['brazil'],  'BRA')
        self.assertEqual(data['brasil'],  'BRA')
        self.assertEqual(data['br'],  'BRA')
        self.assertEqual(data['bra'],  'BRA')
