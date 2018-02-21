import re

_CACHE = {}


def phonemicize(s):
    """Very lite French phonemicization. Try to remove every letter that is not
    significant."""
    if s not in _CACHE:
        rules = (
            ("a(mp|nd|nt)s?$", "an"), # champ(s) > cham
            (r"ngt([aeiouy])", r"nt\1"),  # vingtieme > vintieme
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
            ("oe(?=\\w)", "e"),
            ("(?<=[^0-9])s$", ""),
            ("(?<=u)l?x$", ""),  # eaux, eux, aux, aulx
            ("(?<=u)lt$", "t"),
            ("(?<=[a-z])[dg]$", ""),
            ("(?<=[^es0-9])t$", ""),
            ("(?<=[aeiou])(m)(?=[pbgft])", "n"),
            ("(?<=[a-z]{2})(e$)", ""),  # Remove "e" at last position only if
                                        # it follows two letters?
            ("([aeiouy])n[dt]([^aeiouyr])", "\\1n\\2"), # montbon -> monbon
            (r"([a-z])\1", r"\1"),  # Remove duplicate letters.
        )
        _s = s
        for pattern, repl in rules:
            _s = re.sub(pattern, repl, _s)
#            print(pattern, _s)
        _CACHE[s] = _s
    return s.update(_CACHE[s])
