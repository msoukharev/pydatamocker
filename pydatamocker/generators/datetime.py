from typing import Literal
import pandas as pd
from numpy import arange
from pydatamocker.types import ColumnGenerator


TYPES = {
    'datetime', 'date'
}

default_formatter = {
    'datetime': '%Y-%m-%dT%H:%M:%SZ',
    'date': '%Y-%m-%d'
}

def from_range(start: str, end: str, datatype: Literal['datetime', 'date']) -> ColumnGenerator:
    return lambda size: pd.date_range(start = start, end = end, periods=size)\
        .to_series(index=arange(size)).dt.strftime(default_formatter[datatype])


def from_uniform(start: str, end: str, datatype: Literal['datetime', 'date']) -> ColumnGenerator:
    return lambda size: from_range(start, end, datatype)(size).sample(frac=1).reset_index(drop=True)

def create(**props) -> ColumnGenerator:
    props = dict(props)
    distr = props['distr']
    if distr == 'range':
        return from_range(props['start'], props['end'], datatype=props['datatype'])
    elif distr == 'uniform':
        return from_uniform(props['start'], props['end'], datatype=props['datatype'])
    else:
        raise ValueError('Unsupported distribution: ' + distr)
