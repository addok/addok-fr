from pathlib import Path

from addok.helpers import yielder

from . import utils

phonemicize = yielder(utils.phonemicize)

RESOURCES_ROOT = Path(__file__).parent / 'resources'


def preconfigure(config):
    config.SYNONYMS_PATHS.append(RESOURCES_ROOT / 'synonyms.txt')
    # Set default phonemicize cache size if not already configured
    if not hasattr(config, 'PHONEMICIZE_CACHE_SIZE'):
        config.PHONEMICIZE_CACHE_SIZE = 500_000
