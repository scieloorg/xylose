from unicodedata import normalize


def remove_diacritics(s):
    return normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')


def normalize_value(s):
    s = remove_diacritics(s)
    return s.upper()


def is_a_match(original, normalized):
    if normalize_value(original) == normalize_value(normalized):
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
