from typing import Collection
import re


def assert_nonempty(col: Collection):
    assert len(col) > 0, 'Sample was not created'
    assert len([el for el in col if el != None and str(el) != 'NaN' and el != '']) != 0,\
        'Sample has None and NaN values.'


def assert_unique_count(col: Collection, count: int):
    countunique = len(set(col))
    assert countunique == count, f'Encountered {countunique} elements. Expected {count}.'


def assert_series_superset(col: Collection, super: Collection):
    unique = set(col)
    assert unique.issubset(set(super)), f'Series is not a superset. Values outside : {unique.difference(super)}.'


def assert_elements_type(col: Collection, t: type):
    types = set(type(el) for el in col)
    assert len(types) == 1, f'Several types detected: {types}.'
    acttype = types.pop()
    assert acttype == t, f'Expected type {t} but got {acttype}.'


def assert_match_regex(col: Collection, patternstr: str):
    for el in col:
        assert re.compile(patternstr).match(str(el)), f'Found element not matching the pattern {patternstr}: {el}.'
