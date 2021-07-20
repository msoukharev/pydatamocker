import pandas as pd
from numpy import arange
from .numeric import get_distribution_sampler


ISO_DATETIME = '%Y-%m-%dT%H:%M%:%SZ'
ISO_DATE = '%Y-%m-%d'


def _type_formatter(type_: str):
    if type_ == 'date':
        return ISO_DATE
    if type_ == 'datetime':
        return ISO_DATETIME


_datetime_distr = {
    'range': lambda type_, props: lambda size: pd.date_range(start=props['start'], end=props['end'], periods=size)
        .strftime(_type_formatter(type_))
        .to_series(index=arange(size)),
}


_datetime_distr['uniform'] = (
    lambda type_, props: lambda size: (_datetime_distr['range'])(type_, props)(size).sample(frac=1).reset_index(drop=True)
)


def get_chrono_sampler(mock_type: str, distr: str, **props):
    sampler = _datetime_distr[distr]
    return sampler(mock_type, props)
