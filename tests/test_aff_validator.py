import unittest

from xylose.aff_validator import (
    is_a_match,
    has_conflicts,
    States,
)


class TestIsAMatch(unittest.TestCase):

    def setUp(self):
        self.states = States()

    def test_return_true_if_strings_are_equal(self):
        self.assertTrue(is_a_match("a", "a"))

    def test_return_false_if_strings_are_different(self):
        self.assertFalse(is_a_match("MG", "SP"))

    def test_return_true_for_strings_that_are_different_because_of_the_diacritics(self):
        self.assertTrue(is_a_match("São Paulo", "Sao Paulo"))

    def test_return_true_for_state_which_has_prefixes(self):
        self.assertTrue(is_a_match("State of Rio de Janeiro", "Rio de Janeiro", self.states))

    def test_return_true_for_state_which_has_suffixes(self):
        self.assertTrue(is_a_match("Guangdong Province", "Guangdong", self.states))

    def test_return_true_for_string_which_are_different_because_of_separator_characters(self):
        self.assertTrue(is_a_match("SP", "(SP)"))

    def test_return_true_as_comparing_states_abbrev_and_non_abbrev(self):
        self.assertTrue(is_a_match("Sao Paulo", "SP", self.states))

    def test_return_true_as_comparing_similar_strings(self):
        self.assertTrue(is_a_match("Sao Paulo", "S Paulo", self.states))

    def test_return_true_for_state_abbrev_and_nonnormalized_state(self):
        self.assertTrue(is_a_match("SP", "S Paulo", self.states))


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
