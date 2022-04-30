from typing import Any, Callable, Iterable, Union
from pandas import Series
from math import ceil
from numpy import concatenate, repeat

DISTRIBUTIONS = { 'ordered', 'shuffled' }

def from_shuffled(values: Iterable[Any], weights: Iterable[Union[int, float]]) \
        -> Callable[[int], Series]:
    return lambda size: Series(values).sample(n=size, replace=True, weights=weights).reset_index(drop=True)  # type: ignore

def from_ordered(values: Iterable[Any], counts: Iterable[int]) -> Callable[[int], Series]:
    def aux(size: int, values: Iterable[Any], counts: Iterable[int]):
        weightsum = sum(counts)
        counts = [ ceil(size * (ct / weightsum)) for ct in counts]
        sections = tuple(repeat(val, count) for (val, count) in zip(values, counts))
        arrays = concatenate(sections, axis=None)
        return Series(data=arrays[:size])
    return lambda size: aux(size, values, counts)

def create(**props) -> Callable[[int], Series]:
    values = props['values']
    weights = props.get('weights') or [1] * len(values)
    distr = props.get('distr') or 'ordered'
    if distr == 'shuffled':
        return from_shuffled(values, weights)
    elif distr == 'ordered':
        return from_ordered(values, weights)
    else:
        raise ValueError('Unsupported distribution: '  + distr)
