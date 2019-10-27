import re

_CACHE = {}

compiled_rules = []

def phonemicize(s):
    """Very lite French phonemicization. Try to remove every letter that is not
    significant."""
    global compiled_rules
    if s not in _CACHE:
        if len(compiled_rules) == 0:
            rules = (
                (r"a(mp|nd|nt)s?$", "an"),  # champ(s) > cham
                (r"([aeiouy])mp([^aeiouyr])", r"\1n\2"),  # champvallon -> chanvalon
                (r"ngt([aeiouy])", r"nt\1"),  # vingtieme > vintieme
                (r"ngt", "n"),  # vingt > vin
                (r"((?<=[^g])g|^g)(?=[eyi])", "j"),
                (r"(?<=g)u(?=[aeio])", ""),
                (r"je([aeiouy])", r"j\1"),  # georges -> jorj
                (r"c(?=[^hieyw])", "k"),
                (r"anc$","an"),
                (r"((?<=[^s])ch|(?<=[^0-9])c)$", "k"),  # final "c", "ch",
                                                    # but not "sch" and not 10c.
                (r"(?<=[aeiouy])s(?=[aeiouy])", "z"),
                (r"((?<=[^0-9])q|^q)u?", "k"),
                (r"cc(?=[ie])", "s"),  # Others will hit the c => k and deduplicate
                ("ck", "k"),
                ("ph", "f"),
                (r"th$", "te"),  # This t sounds.
                (r"(?<=[^sc0-9])h", ""),
                (r"^h(?=.)+", ""),
                ("sc", "s"),
                ("sh", "ch"),
                (r"((?<=[^0-9])w|^w)", "v"),
                (r"c(?=[eiy])", "s"),
                (r"(?<=[^0-9])y", "i"),
                ("esn", "en"),
                (r"oe(?=\w)", "e"),
                (r"(?<=[^0-9])s$", ""),
                (r"(?<=u)l?x$", ""),  # eaux, eux, aux, aulx
                (r"(?<=u)lt$", "t"),
                (r"(?<=[a-z])[dg]$", ""),
                (r"(?<=[^es0-9])t$", ""),
                (r"(?<=[aeiou])(m)(?=[pbgft])", "n"),
                (r"(?<=[a-z]{2})(e$)", ""),  # Remove "e" at last position only if
                                            # it follows two letters?
                (r"([aeiouy])n[dt]([^aeiouyr])", r"\1n\2"),  # montbon -> monbon
                (r"([a-z])\1", r"\1"),  # Remove duplicate letters.
            )
            for pattern, repl in rules:
                compiled_rules.append((re.compile(pattern), repl))
        _s = s
        for pattern, repl in compiled_rules:
            _s = pattern.sub(repl, _s)
        _CACHE[s] = _s
    return s.update(_CACHE[s])
