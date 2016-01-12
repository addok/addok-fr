from addok.helpers import yielder
from addok import hooks
from .utils import phonemicize


@hooks.register
def addok_configure(config):
    config.PROCESSORS.append(yielder(phonemicize))
