from typing import Iterable
from pandas import Series


def assert_nonempty_series(ser: Series):
    assert len(ser) > 0,                'Sample was not created'
    assert ser.isna().count() != 0,     'Sample has NaN values'


def assert_series_superset(ser: Series, super: Iterable):
    unique = set(ser.unique())
    assert unique.issubset(set(super)), f'Series is not a superset. Values outside : {unique.difference(super)}.'
