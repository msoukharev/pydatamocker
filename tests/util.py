from typing import Any, Callable, Collection, Iterable, TypeVar
import re


T= TypeVar('T')


def assert_(subj: T, pred: Callable[[T], bool], err_msg: Callable[[T], str]):
    assert bool(pred(subj)), err_msg(subj)


def assert_all(subjs: Collection[T], pred: Callable[[T], bool], err_msg: Callable[[T], str]):
    for subj in subjs:
        assert pred(subj), err_msg(subj)


def assert_any(subjs: Collection[T], pred: Callable[[T], bool], err_msg: str):
    for subj in subjs:
        if pred(subj):
            return
    assert False, err_msg


def eq(exp: Any):
    return lambda act: exp == act


def order(exp: Collection):
    def inner(act: Collection):
        if len(exp) != len(act):
            return False
        for a, b in zip(exp, act):
            if a != b:
                return False
        return True
    return inner

def mismatch(exp: Any):
    return lambda act: f'Expected {exp} but got {act}'


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
