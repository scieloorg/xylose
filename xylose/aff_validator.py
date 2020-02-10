from unicodedata import normalize


def remove_diacritics(s):
    return normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')


def remove_suffixes_and_prefixes(state):
    for term in [" PROVINCE", "PROVINCIA DE ", "STATE OF ", " STATE"]:
        state = state.replace(term, "")
    return state


def normalize_value(s):
    s = remove_diacritics(s)
    s = s.upper()
    s = remove_suffixes_and_prefixes(s)
    return s


def is_a_match(original, normalized):
    original = normalize_value(original)
    normalized = normalize_value(normalized)

    if original == normalized:
        return True
    return False


def has_conflicts(original_aff, normaff):
    if original_aff:
        conflicts = []
        for label in ["country_iso_3166", "state", "city"]:

            original = original_aff.get(label)
            normalized = normaff.get(label)

            if original and normalized:

                if is_a_match(original, normalized):
                    continue

                conflicts.append((label, original, normalized))

        return conflicts
