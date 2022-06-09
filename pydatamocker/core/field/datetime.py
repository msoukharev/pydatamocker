import pandas as pd
from numpy import arange
from typing import Optional
from pydatamocker.types import FieldGenerator


TYPES = {
    'datetime'
}


default_formatter = {
    'datetime': '%Y-%m-%dT%H:%M:%SZ',
    'date': '%Y-%m-%d'
}


def from_range(start: str, end: str, format: Optional[str]) -> FieldGenerator:
    return lambda size: pd.date_range(start=start, end=end, periods=size)\
        .to_series(index=arange(size)).dt.strftime(default_formatter[format or 'datetime'])


def from_uniform(start: str, end: str, format: Optional[str]) -> FieldGenerator:
    return lambda size: from_range(start, end, format)(size).sample(frac=1).reset_index(drop=True)
