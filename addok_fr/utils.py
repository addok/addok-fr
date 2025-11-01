import re
from functools import lru_cache

from addok import config

RULES = (
    ("(?<=a)(mp|nd|nt)s?$", "n"),  # champ(s) > cham
    (r"([aeiouy])mp(?=[^aeiouyr])", r"\1n"),  # champvallon -> chanvalon
    (r"ngt(?=[aeiouy])", "nt"),  # vingtieme > vintieme
    (r"ngt", "n"),  # vingt > vin
    ("((?<=[^g])g|^g)(?=[eyi])", "j"),
    ("(?<=g)u(?=[aeio])", ""),
    (r"(?<=ei)gn([aeiouy])", r"ni\1"),  # seigneur -> senieur (only after ei specifically)
    (r"je([aeiouy])", r"j\1"),  # georges -> jorj
    ("c(?=[^hieyw])", "k"),
    (r"anc$", "an"),  # blanc -> blan
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
    (r"((?<=[^0-9])y|^y)", "i"),  # also handle y at beginning
    ("esn", "en"),
    (r"eim( |$)", "aim"),  # pforzheim -> pforzaim
    (r"(ae|ei)(?=\w)", "e"),  # improved ae/ei handling
    (r"oeufs( |$)", "eu"),  # special case for oeufs
    (r"oeu?(?=\w)", "eu"),  # oe/oeu -> eu
    ("(?<=[^0-9])s$", ""),
    ("(?<=u)l?x$", ""),  # eaux, eux, aux, aulx
    ("(?<=u)lt$", "t"),
    ("(?<=[a-z])[dg]$", ""),
    ("(?<=[^es0-9])t$", ""),
    ("(?<=[aeiou])(m)(?=[pbgft])", "n"),  # m -> n before labial/dental consonants (e.g., impossible -> inpossible)
    ("(?<=[a-z]{2})(e$)", ""),  # Remove "e" at last position only if
                                # it follows two letters?
    (r"(?<=[aeiouy])n[dt](?=[^aeiouyr])", "n"),  # montbon -> monbon
    (r"([a-z])\1+", r"\1"),  # Remove duplicate letters (one or more repetitions)
)
COMPILED = list((re.compile(pattern), replacement) for pattern, replacement in RULES)

# Cache will be initialized lazily to allow configuration via preconfigure()
_phonemicize_cached = None


def _get_cached_function():
    """Get or create the cached phonemicize function.
    
    This lazy initialization ensures the cache size is read after preconfigure()
    has run, avoiding race conditions.
    """
    global _phonemicize_cached
    if _phonemicize_cached is None:
        cache_size = getattr(config, 'PHONEMICIZE_CACHE_SIZE', 500_000)
        
        @lru_cache(maxsize=cache_size)
        def _impl(text):
            """Apply phonemicization rules to a string.
            
            This function is cached with LRU (Least Recently Used) strategy.
            Cache size is configurable via config.PHONEMICIZE_CACHE_SIZE.
            Default: 500,000 entries (~86 MB), suitable for ~500K unique words.
            """
            result = text
            for pattern, repl in COMPILED:
                result = pattern.sub(repl, result)
            return result
        
        _phonemicize_cached = _impl
    return _phonemicize_cached


def _phonemicize_string(text):
    """Wrapper to call the cached function."""
    return _get_cached_function()(text)


def phonemicize(s):
    """Very lite French phonemicization. Try to remove every letter that is not
    significant.

    Takes a Token, applies phonemicization rules (cached), and returns
    a new Token with the phonemicized value while preserving metadata
    (position, is_last, raw, etc.).
    """
    phonemicized = _phonemicize_string(str(s))
    return s.update(phonemicized)
