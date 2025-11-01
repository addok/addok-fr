# addok-fr

Addok plugin for improved French geocoding with phonetic normalization and French-specific synonym handling.

## Features

- **Phonetic normalization**: French-optimized phonetic processor that handles typos and spelling variations in address searches
- **French synonyms**: Pre-configured synonym database for common French address terms (rue, avenue, boulevard, etc.)

## Installation

    pip install addok-fr


## Configuration

### Enable the phonemicize processor

Add `phonemicize` into PROCESSORS_PYPATHS:

```python
PROCESSORS_PYPATHS = [
    …,
    'addok_fr.phonemicize'
]
```

### Cache configuration (optional)

The phonemicize processor uses an LRU cache to improve performance. By default, the cache can hold up to 500,000 entries (~86 MB of memory), which is suitable for approximately 500,000 unique words.

You can adjust the cache size in your Addok configuration file:

```python
PHONEMICIZE_CACHE_SIZE = 500_000  # Default value
```

**Recommendations:**
- **500K entries** (~86 MB): Default, suitable for most French address datasets
- **1M entries** (~172 MB): For larger datasets with more unique words
- **250K entries** (~43 MB): For memory-constrained environments

The cache uses an LRU (Least Recently Used) eviction strategy, meaning the most frequently used words will remain cached even if the maximum size is reached
