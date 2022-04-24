from typing import Iterable


def create(table_descriptor: dict) -> Iterable:
    names = set()
    specs = []
    for fs in table_descriptor['fields']:
        name = fs['name']
        if name in names:
            raise ValueError('Duplicated name: ' + name)
        specs.append(fs)
    return specs
