from typing import Iterable
from pydatamocker.types import FieldToken


def create(table_descriptor: dict) -> Iterable[FieldToken]:
    names = set()
    specs: Iterable[FieldToken] = []
    for fs in table_descriptor['fields']:
        name = fs['name']
        if name in names:
            raise ValueError('Duplicated name: ' + name)
        names.add(name)
        specs.append(fs)
    return specs
