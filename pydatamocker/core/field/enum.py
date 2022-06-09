from typing import Any, List, Optional, Union
from pandas import Series
from math import ceil
from numpy import concatenate, repeat
from pydatamocker.types import FieldGenerator


DISTRIBUTIONS = {'ordered', 'shuffled'}


def from_enum(
    values: List[Any],
    counts: Optional[List[Union[int, float]]] = None,
    shuffle: bool = True
) -> FieldGenerator:
    weights: List[Union[int, float]] = counts or [1] * len(values)
    if shuffle:
        return lambda size: Series(values)\
            .sample(n=size, replace=True, weights=weights)\
            .reset_index(drop=True)
    else:
        def aux(size: int, values: List[Any], counts__: List[Union[int, float]]):
            weightsum = sum(counts__)
            counts_: List[int] = [ceil(size * (ct / weightsum)) for ct in counts__]
            sections = tuple(repeat(val, count) for (val, count) in zip(values, counts_))
            arrays = concatenate(sections, axis=None)
            return Series(data=arrays[:size])
        return lambda size: aux(size, values, weights)
