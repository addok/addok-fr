from pathlib import Path

from addok.helpers import yielder

from . import utils

phonemicize = yielder(utils.phonemicize)

RESOURCES_ROOT = Path(__file__).parent / 'resources'


def preconfigure(config):
    config.SYNONYMS_PATH = RESOURCES_ROOT / 'synonyms.txt'
