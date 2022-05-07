from typing import Any, Iterable, Union
from pandas import Series
from math import ceil
from numpy import concatenate, repeat
from pydatamocker.types import ColumnGenerator, EnumFieldSpec


DISTRIBUTIONS = { 'ordered', 'shuffled' }


def from_shuffled(values: Iterable[Any], weights: Iterable[Union[int, float]]) \
        -> ColumnGenerator:
    return lambda size: Series(values).sample(n=size, replace=True, weights=weights).reset_index(drop=True)  # type: ignore


def from_ordered(values: Iterable[Any], counts: Iterable[int]) -> ColumnGenerator:
    def aux(size: int, values: Iterable[Any], counts: Iterable[int]):
        weightsum = sum(counts)
        counts = [ ceil(size * (ct / weightsum)) for ct in counts]
        sections = tuple(repeat(val, count) for (val, count) in zip(values, counts))
        arrays = concatenate(sections, axis=None)
        return Series(data=arrays[:size])
    return lambda size: aux(size, values, counts)


def create(spec: EnumFieldSpec) -> ColumnGenerator:
    values = spec['value']['values']
    weights = spec['value'].get('weights') or [1] * len(values)
    distr = spec['value'].get('distr') or 'ordered'
    if distr == 'shuffled':
        return from_shuffled(values, weights)
    elif distr == 'ordered':
        return from_ordered(values, weights)
    else:
        raise ValueError('Unsupported distribution: '  + distr)
