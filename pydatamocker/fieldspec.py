from typing import Collection
from pydatamocker.types import FieldToken


def translate(table_descriptor: dict) -> Collection[FieldToken]:
    names = set()
    specs: Collection[FieldToken] = []
    for fs in table_descriptor['fields']:
        name = fs['name']
        if name in names:
            raise ValueError('Duplicated name: ' + name)
        names.add(name)
        specs.append(fs)
    return specs
