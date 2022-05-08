import pandas as pd
from numpy import arange
from pydatamocker.types import ColumnGenerator, FieldParams


TYPES = {
    'datetime'
}


default_formatter = {
    'datetime': '%Y-%m-%dT%H:%M:%SZ',
    'date': '%Y-%m-%d'
}


def from_range(start: str, end: str, format: str) -> ColumnGenerator:
    return lambda size: pd.date_range(start = start, end = end, periods=size)\
        .to_series(index=arange(size)).dt.strftime(format)


def from_uniform(start: str, end: str, format: str) -> ColumnGenerator:
    return lambda size: from_range(start, end, format)(size).sample(frac=1).reset_index(drop=True)


def create(field: FieldParams) -> ColumnGenerator:
    try:
        distr = field['distr']
        distr_name = distr['name']
        format = field.get('format')
        format = format and \
            (format in default_formatter and default_formatter[format] or format)\
                or default_formatter['datetime']
        if distr_name == 'range':
            return from_range(distr['start'], distr['end'], format=format)
        elif distr_name == 'uniform':
            return from_uniform(distr['start'], distr['end'], format=format)
        else:
            raise ValueError(f"Unsupported distribution: {distr['name']}")
    except KeyError as kerr:
        raise kerr
