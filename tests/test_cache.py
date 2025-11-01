import pytest

from addok.helpers.text import Token
from addok_fr.utils import phonemicize, _phonemicize_string


def test_cache_hits_on_repeated_calls():
    """Test that the LRU cache works correctly on repeated calls."""
    # Clear the cache before testing
    _phonemicize_string.cache_clear()

    # First call should be a cache miss
    token1 = Token('paris')
    result1 = phonemicize(token1)
    cache_info_after_first = _phonemicize_string.cache_info()

    assert str(result1) == 'pari'
    assert cache_info_after_first.misses == 1
    assert cache_info_after_first.hits == 0

    # Second call with same value should be a cache hit
    token2 = Token('paris')
    result2 = phonemicize(token2)
    cache_info_after_second = _phonemicize_string.cache_info()

    assert str(result2) == 'pari'
    assert cache_info_after_second.misses == 1
    assert cache_info_after_second.hits == 1


def test_cache_preserves_token_metadata():
    """Test that caching doesn't affect Token metadata preservation."""
    _phonemicize_string.cache_clear()

    # First call
    token1 = Token('lyon', position=0, is_last=False, raw='Lyon')
    result1 = phonemicize(token1)

    assert str(result1) == 'lion'
    assert result1.position == [0]
    assert result1.is_last is False
    assert result1.raw == 'Lyon'

    # Second call with different metadata but same value
    token2 = Token('lyon', position=5, is_last=True, raw='LYON')
    result2 = phonemicize(token2)

    assert str(result2) == 'lion'
    assert result2.position == [5]
    assert result2.is_last is True
    assert result2.raw == 'LYON'


def test_cache_max_size():
    """Test that the cache has the expected maximum size."""
    cache_info = _phonemicize_string.cache_info()
    assert cache_info.maxsize == 500_000


def test_cache_can_be_cleared():
    """Test that the cache can be cleared."""
    _phonemicize_string.cache_clear()

    # Add some entries
    phonemicize(Token('paris'))
    phonemicize(Token('lyon'))
    phonemicize(Token('marseille'))

    cache_info = _phonemicize_string.cache_info()
    assert cache_info.currsize == 3

    # Clear the cache
    _phonemicize_string.cache_clear()

    cache_info_after = _phonemicize_string.cache_info()
    assert cache_info_after.currsize == 0
    assert cache_info_after.hits == 0
    assert cache_info_after.misses == 0
