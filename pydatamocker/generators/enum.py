from pandas import Series
from math import ceil
from numpy import concatenate, repeat

DISTRIBUTIONS = { 'ordered', 'shuffle' }

def generate(**props) -> Series:
    values = props['values']
    weights = props.get('weights') or [1] * len(values)
    size = props['size']
    distr = props.get('distr')
    if distr == 'shuffle':
        weightsum = sum(weights)
        counts = [ ceil(size * (w / weightsum)) for w in weights ]
        sections = tuple(repeat(val, count) for (val, count) in zip(values, counts))
        arrays = concatenate(sections, axis=None)
        return Series(data=arrays[:size])
    else:
        distr = 'ordered'
        return Series(values).sample(n=size, replace=True, weights=weights).reset_index(drop=True)
