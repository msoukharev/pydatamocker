import pandas as pd
from numpy import arange
from pydatamocker.types import ColumnGenerator, DatetimeFieldSpec


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


def create(spec: DatetimeFieldSpec) -> ColumnGenerator:
    value = spec['value']
    distr = value['distr']
    format = value.get('format') and \
        (value['format'] in default_formatter and default_formatter[value['format']] or value['format'])\
            or default_formatter['datetimes']
    if distr == 'range':
        return from_range(value['start'], value['end'], format=format)
    elif distr == 'uniform':
        return from_uniform(value['start'], value['end'], format=format)
    else:
        raise ValueError('Unsupported distribution: ' + distr)
