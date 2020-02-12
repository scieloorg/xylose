# coding: utf-8
import os
from difflib import SequenceMatcher
from unicodedata import normalize


def remove_diacritics(s):
    try:
        s = normalize('NFKD', s)
    except TypeError:
        s = normalize('NFKD', unicode(s, "utf-8"))
    finally:
        return s.encode('ASCII', 'ignore').decode('ASCII')


def remove_suffixes_and_prefixes(state):
    for term in [" PROVINCE", "PROVINCIA DE ", "STATE OF ", " STATE"]:
        state = state.replace(term, "")
    return state


def remove_non_alpha_characters(s):
    # Remove caracteres como vírgulas, pontos, parênteses etc
    return "".join([c for c in s if c.isalpha() or c in [" ", "-"]])


def similarity_ratio(value1, value2):
    s = SequenceMatcher(None, value1, value2)
    return s.ratio()


def normalize_value(s):
    s = remove_diacritics(s)
    s = s.upper()
    s = remove_non_alpha_characters(s)
    return s


class States:

    def __init__(self):
        self._states = {}
        self.load()

    def load(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/assets/states_abbrev.csv") as fp:
            for row in fp.readlines():
                row = row.strip()
                if "," in row:
                    name, abbrev = row.split(",")
                    name = remove_diacritics(name)
                    name = name.upper()
                    self._states[name] = abbrev

    def get_state_abbrev(self, state):
        return self._states.get(state)

    def get_state_abbrev_by_similarity(self, state):
        similar = [
            (similarity_ratio(name, state), abbrev)
            for name, abbrev in self._states.items()
        ]
        similar = sorted(similar)
        if similar[-1][0] > 0.8:
            return similar[-1][1]

    def normalize(self, state):
        state = remove_suffixes_and_prefixes(state)
        state_abbrev = (
            self.get_state_abbrev(state) or
            self.get_state_abbrev_by_similarity(state) or
            state
        )
        return state_abbrev


def is_a_match(original, normalized, states=None):
    original = normalize_value(original)
    normalized = normalize_value(normalized)
    if original == normalized:
        return True

    if similarity_ratio(original, normalized) > 0.8:
        return True

    if states and hasattr(states, 'normalize'):
        original = states.normalize(original)
        normalized = states.normalize(normalized)
        if original == normalized:
            return True
    return False


STATES = States()


def has_conflicts(original_aff, normaff):
    if original_aff:
        conflicts = []
        for label in ["country_iso_3166", "state", "city"]:

            original = original_aff.get(label)
            normalized = normaff.get(label)

            if original and normalized:
                states = STATES if label == "state" else None
                if is_a_match(original, normalized, states):
                    continue

                conflicts.append((label, original, normalized))

        return conflicts
