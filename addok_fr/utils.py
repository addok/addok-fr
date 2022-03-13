import re

_CACHE = {}
RULES = (
    ("(?<=a)(mp|nd|nt)s?$", "n"),  # champ(s) > cham
    (r"ngt(?=[aeiouy])", "nt"),  # vingtieme > vintieme
    (r"ngt", "n"),  # vingt > vin
    ("((?<=[^g])g|^g)(?=[eyi])", "j"),
    ("(?<=g)u(?=[aeio])", ""),
    ("c(?=[^hieyw])", "k"),
    ("((?<=[^s])ch|(?<=[^0-9])c)$", "k"),  # final "c", "ch",
    # but not "sch" and not 10c.
    ("(?<=[aeiouy])s(?=[aeiouy])", "z"),
    ("((?<=[^0-9])q|^q)u?", "k"),
    ("cc(?=[ie])", "s"),  # Others will hit the c => k and deduplicate
    ("ck", "k"),
    ("ph", "f"),
    ("th$", "te"),  # This t sounds.
    ("(?<=[^sc0-9])h", ""),
    ("^h(?=.)+", ""),
    ("sc", "s"),
    ("sh", "ch"),
    ("((?<=[^0-9])w|^w)", "v"),
    ("c(?=[eiy])", "s"),
    ("(?<=[^0-9])y", "i"),
    ("esn", "en"),
    (r"oe(?=\w)", "e"),
    ("(?<=[^0-9])s$", ""),
    ("(?<=u)l?x$", ""),  # eaux, eux, aux, aulx
    ("(?<=u)lt$", "t"),
    ("(?<=[a-z])[dg]$", ""),
    ("(?<=[^es0-9])t$", ""),
    ("(?<=[aeiou])(m)(?=[pbgf])", "n"),
    ("(?<=[a-z]{2})(e$)", ""),  # Remove "e" at last position only if
                                # it follows two letters?
    (r"(?<=[aeiouy])n[dt](?=[^aeiouyr])", "n"),  # montbon -> monbon
    (r"(\D)(?=\1)", ""),  # Remove duplicate letters.
)
COMPILED = list((re.compile(pattern), replacement) for pattern, replacement in RULES)


def phonemicize(s):
    """Very lite French phonemicization. Try to remove every letter that is not
    significant."""
    if s not in _CACHE:
        _s = s
        for pattern, repl in COMPILED:
            _s = pattern.sub(repl, _s)
        _CACHE[s] = _s
    return s.update(_CACHE[s])
