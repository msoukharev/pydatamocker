from typing import Union
import numpy as np
from pandas import Series
from pydatamocker.types import ColumnGenerator, IntegerFieldSpec, NumericFieldSpec


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


def create(spec: NumericFieldSpec) -> ColumnGenerator:
    type_ = spec['type']
    value = spec['value']['distr']
    distr_name = value['name']
    if type_ == 'float':
        if distr_name == 'normal':
            return from_normal_float(value['mean'], value['std'])
        if distr_name == 'uniform':
            return from_uniform_float(value['min'], value['max'])
        if distr_name == 'range':
            return from_range_float(value['start'], value['end'])
        else:
            raise ValueError(f'Unsupported distribution {distr_name} for type float')
    elif type_ == 'integer':
        if distr_name == 'normal':
            return from_normal_integer(value['mean'], value['std'])
        if distr_name == 'uniform':
            return from_uniform_integer(value['min'], value['max'])
        if distr_name == 'range':
            return from_range_integer(value['start'], value['end'])
        if distr_name == 'binomial':
            return from_binomial_integer(value['n'], value['p'])
        else:
            raise ValueError(f'Unsupported distribution {distr_name} for type integer')
    else:
        raise ValueError(f'Unsupported type ' + type_)
