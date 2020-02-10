import unittest

from xylose.aff_validator import (
    is_a_match,
    has_conflicts,
)


class TestIsAMatch(unittest.TestCase):
    def test_return_true_if_strings_are_equal(self):
        self.assertTrue(is_a_match("a", "a"))

    def test_return_false_if_strings_are_different(self):
        self.assertFalse(is_a_match("MG", "SP"))

    def test_return_true_for_strings_that_are_different_because_of_the_diacritics(self):
        self.assertTrue(is_a_match("São Paulo", "Sao Paulo"))


class TestHasConflicts(unittest.TestCase):
    def test_return_conflicts_if_aff_data_do_not_match(self):
        norm_aff = {
            "state": "DF",
            "city": "",
            "country_iso_3166": "BR",
            "institution": "Universidade",
            "index": "A01",
        }
        original_aff = {
            "state": "SP",
            "city": "São Paulo",
            "country_iso_3166": "BR",
            "institution": "Universidade de São Paulo",
            "index": "A01",
        }
        expected = [("state", "SP", "DF")]
        result = has_conflicts(original_aff, norm_aff)
        self.assertEqual(expected, result)
