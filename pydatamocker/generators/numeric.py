from typing import Union
import numpy as np
from pandas import Series
from pydatamocker.generators.datetime import from_uniform
from pydatamocker.types import ColumnGenerator, FieldParams, UnaryFilter
from pydatamocker.util.switch import switch


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


def from_const(const: Union[float, int]) -> ColumnGenerator:
    return lambda size: Series(np.repeat(const, size))


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


def from_numeric(params: FieldParams) -> ColumnGenerator:
    try:
        type_ = params['type']
        distr = params.get('distr')
        const = params.get('const')
        filters = params.get('filters')
        if distr:
            name = distr['name']
            if type_ == 'float':
                gen = switch(name, {
                    'normal': lambda: from_normal_float(distr['mean'], distr['max']),
                    'uniform': lambda: from_uniform_float(distr['min'], distr['max']),
                    'range': lambda: from_range_float(distr['start'], distr['end'])
                })()
            elif type_ == 'integer':
                gen = switch(name, {
                    'normal': lambda: from_normal_integer(distr['mean'], distr['std']),
                    'uniform': lambda: from_uniform_integer(distr['min'], distr['max']),
                    'range': lambda: from_range_integer(distr['start'], distr['end']),
                    'binomial': lambda: from_binomial_integer(distr['n'], distr['p'])
                })()
            else:
                raise ValueError(f'Unsupported type ' + type_)
        elif const is not None:
            gen = from_const(params['const'])
        else:
            raise ValueError(f'No distr or constant is provided')
        if filters:
            for f in filters:
                gen = apply_filter(gen, f)
        return gen
    except KeyError as kerr:
        raise kerr


def apply_add(gen: ColumnGenerator, params: FieldParams) -> ColumnGenerator:
    return lambda size: gen(size) + from_numeric(params)(size)


def apply_subtract(gen: ColumnGenerator, params: FieldParams) -> ColumnGenerator:
    return lambda size: gen(size) - from_numeric(params)(size)


def apply_subtract_from(gen: ColumnGenerator, params: FieldParams) -> ColumnGenerator:
    return lambda size: from_numeric(params)(size) - gen(size)


def apply_multiply(gen: ColumnGenerator, params: FieldParams) -> ColumnGenerator:
    return lambda size: gen(size) * from_numeric(params)(size)


def apply_floor(gen: ColumnGenerator, params: FieldParams) -> ColumnGenerator:
    try:
        return lambda size: gen(size).map(lambda x: max(params['const'], x))
    except KeyError as _:
        raise ValueError('Missing value for const')


def apply_ceiling(gen: ColumnGenerator, params: FieldParams) -> ColumnGenerator:
    try:
        return lambda size: gen(size).map(lambda x: min(params['const'], x))
    except KeyError as _:
        raise ValueError('Missing value for const')


def apply_filter(generator: ColumnGenerator, filter: UnaryFilter) -> ColumnGenerator:
    op = filter['operator']
    arg = filter['argument']
    return switch(op,
        {
            'add': lambda: apply_add(generator, arg),
            'subtract': lambda: apply_subtract(generator, arg),
            'subtract_from': lambda: apply_subtract(generator, arg),
            'multiply': lambda: apply_multiply(generator, arg),
            'floor': lambda: apply_floor(generator, arg),
            'ceiling': lambda: apply_ceiling(generator, arg)
        }
    )()
