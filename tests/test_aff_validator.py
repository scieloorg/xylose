import unittest

from xylose.aff_validator import (
    is_a_match,
)


class TestIsAMatch(unittest.TestCase):

    def test_return_true_if_strings_are_equal(self):
        self.assertTrue(is_a_match("a", "a"))

    def test_return_false_if_strings_are_different(self):
        self.assertFalse(is_a_match("MG", "SP"))
