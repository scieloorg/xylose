

def normalize_value(s):
    return s.upper()


def is_a_match(original, normalized):
    if normalize_value(original) == normalize_value(normalized):
        return True
    return False
