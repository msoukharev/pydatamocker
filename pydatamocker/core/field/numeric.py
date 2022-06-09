from typing import Union, cast
import numpy as np
from pandas import Series
from pydatamocker.types import FieldGenerator


def _range_step(min: int, max: int, size: int):
    return (max - min) / size


def from_normal(mean: float, std: float) -> FieldGenerator:
    return lambda size: Series(np.random.normal(mean, std, size))


def from_uniform(min_: Union[int, float], max_: Union[int, float]) -> FieldGenerator:
    if isinstance(min_, (int)) and isinstance(max_, (int)):
        return lambda size: Series(np.random.randint(min_, max_, size))
    else:
        return lambda size: Series(np.random.uniform(min_, max_, size))


def from_range(start: Union[int, float], end: Union[int, float]) -> FieldGenerator:
    if isinstance(start, (int)) and isinstance(end, (int)):
        return lambda size: Series(
            np.arange(start, end, _range_step(start, end, size)).astype(int)[:size]
        )
    else:
        return lambda size: Series(
            np.arange(start, end, _range_step(round(start), round(end), size)).astype(float)[:size]
        )


def from_const(const: Union[float, int]) -> FieldGenerator:
    return lambda size: Series(np.repeat(const, size))


def from_binomial(n: int, p: float) -> FieldGenerator:
    return lambda size: Series(np.random.binomial(n, p, size))


def from_range_integer(start: int, end: int) -> FieldGenerator:
    return lambda size: Series(
        np.arange(start, end, _range_step(start, end, size)).astype(int)[:size]
    )


def add(gen: FieldGenerator, mod: Union[FieldGenerator, int, float]) -> FieldGenerator:
    if callable(mod):
        return lambda size: gen(size) + cast(FieldGenerator, mod)(size)
    elif isinstance(mod, (int, float)):
        return lambda size: gen(size) + mod
    else:
        raise TypeError(f'Unsupported modificator type {type(mod)}.')


def subtract(gen: FieldGenerator, mod: Union[FieldGenerator, int, float]) -> FieldGenerator:
    if callable(mod):
        return lambda size: gen(size) - cast(FieldGenerator, mod)(size)
    elif isinstance(mod, (int, float)):
        return lambda size: gen(size) - mod
    else:
        raise TypeError(f'Unsupported modificator type {type(mod)}.')


def subtract_from(gen: FieldGenerator, mod: Union[FieldGenerator, int, float]) -> FieldGenerator:
    if callable(mod):
        return lambda size: cast(FieldGenerator, mod)(size) - gen(size)
    elif isinstance(mod, (int, float)):
        return lambda size: mod - gen(size)
    else:
        raise TypeError(f'Unsupported modificator type {type(mod)}.')


def multiply(gen: FieldGenerator, mod: Union[FieldGenerator, int, float]) -> FieldGenerator:
    if callable(mod):
        return lambda size: cast(FieldGenerator, mod)(size) * gen(size)
    elif isinstance(mod, (int, float)):
        return lambda size: gen(size) * mod
    else:
        raise TypeError(f'Unsupported modificator type {type(mod)}.')


def floor(gen: FieldGenerator, mod: Union[int, float]) -> FieldGenerator:
    return lambda size: gen(size).map(lambda x: max(x, mod))


def ceiling(gen: FieldGenerator, mod: Union[int, float]) -> FieldGenerator:
    return lambda size: gen(size).map(lambda x: min(x, mod))


def round_(gen: FieldGenerator, mod: int) -> FieldGenerator:
    if mod < 0:
        raise ValueError(f'Cannot use negative integer for rounding: {mod}')
    return \
        (lambda size: gen(size).round(mod)) if mod != 0 \
        else (lambda size: gen(size).round(mod).astype(int))
