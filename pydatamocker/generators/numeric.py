import numpy as np
from pandas import Series
from pydatamocker.types import ColumnGenerator


TYPES = { 'float', 'integer' }


def _range_step(min: int, max: int, size: int):
    return (max - min) / size


def from_normal_float(mean: float, std: float) -> ColumnGenerator:
    return lambda size: Series(np.random.normal(mean, std, size))


def from_uniform_float(min_: float, max_: float) -> ColumnGenerator:
    return lambda size: Series(np.random.uniform(min_, max_, size))


def from_range_float(start: float, end: float) -> ColumnGenerator:
    return lambda size: Series(np.arange(start, end,
        _range_step(round(start), round(end), size)).astype(float)[:size]
    )


def from_uniform_integer(min: int, max: int) -> ColumnGenerator:
    return lambda size: Series(np.random.randint(min, max, size))


def from_binomial_integer(n: int, p: float) -> ColumnGenerator:
    return lambda size: Series(np.random.binomial(n, p, size))


def from_range_integer(start: int, end: int) -> ColumnGenerator:
    return lambda size: Series(
        np.arange(start, end, _range_step(start, end, size)).astype(int)[:size]
    )


def from_normal_integer(mean: int, std: float) -> ColumnGenerator:
    # binomial approximation to normal
    # mean = n p
    # std = n p (1 - p)
    p = 1 - (std / mean)
    n = round(mean / p)
    return from_binomial_integer(n, p)


def create(**props) -> ColumnGenerator:
    datatype = props['datatype']
    distr = props['distr']

    if datatype == 'float':
        if distr == 'normal':
            return from_normal_float(props['mean'], props['std'])
        if distr == 'uniform':
            return from_uniform_float(props['min'], props['max'])
        if distr == 'range':
            return from_range_float(props['start'], props['end'])
        else:
            raise ValueError(f'Unsupported distribution {distr} for type float')
    elif datatype == 'integer':
        if distr == 'normal':
            return from_normal_integer(props['mean'], props['std'])
        if distr == 'uniform':
            return from_uniform_integer(props['min'], props['max'])
        if distr == 'range':
            return from_range_integer(props['start'], props['end'])
        if distr == 'binomial':
            return from_binomial_integer(props['n'], props['p'])
        else:
            raise ValueError(f'Unsupported distribution {distr} for type integer')
    else:
        raise ValueError(f'Unsupported type ' + datatype)
