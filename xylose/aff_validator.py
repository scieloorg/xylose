from unicodedata import normalize


def remove_diacritics(s):
    return normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')


def remove_suffixes_and_prefixes(state):
    for term in [" PROVINCE", "PROVINCIA DE ", "STATE OF ", " STATE"]:
        state = state.replace(term, "")
    return state


def remove_non_alpha_characters(s):
    # Remove caracteres como vírgulas, pontos, parênteses etc
    return "".join([c for c in s if c.isalpha() or c in [" ", "-"]])


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
        with open("xylose/states_abbrev.csv") as fp:
            for row in fp.readlines():
                row = row.strip()
                if "," in row:
                    name, abbrev = row.split(",")
                    name = remove_diacritics(name)
                    name = name.upper()
                    self._states[name] = abbrev

    def get_state_abbrev(self, state):
        state = normalize_value(state)
        state = remove_suffixes_and_prefixes(state)
        return self._states.get(state, state)


def is_a_match(original, normalized, states=None):
    original = normalize_value(original)
    normalized = normalize_value(normalized)
    if original == normalized:
        return True

    if states and hasattr(states, 'get_state_abbrev'):
        original_abbrev = states.get_state_abbrev(original)
        normalized_abbrev = states.get_state_abbrev(normalized)
        if original_abbrev == normalized_abbrev:
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
