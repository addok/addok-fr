# Addok plugin for French support

## Installation

    # No pypi release yet.
    pip install git+https://github.com/addok/addok-france


## Configuration

- Add `phonemicize` into PROCESSORS:

    PROCESSORS = [
        …,
        'addok_fr.phonemicize'
    ]
