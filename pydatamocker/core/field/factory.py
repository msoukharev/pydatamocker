from typing import Dict

from pandas import Series
import pydatamocker.core.field.numeric as numeric
import pydatamocker.core.field.dataset as dataset
import pydatamocker.core.field.enum as enum
import pydatamocker.core.field.datetime as dt
from pydatamocker.types import FieldGenerator, FieldName, Value


def get_generator(val: Value, generators: Dict[FieldName, Series] = {}) -> FieldGenerator:
    match val:
        case {'dataset': {'name': datasetname, **rest}}:
            gen = dataset.from_dataset(datasetname, restrict=rest.get('restrict'))
        case {'normal': {'mean': mean, 'std': std}}:
            gen = numeric.from_normal(mean, std)
        case {'binomial': {'n': n, 'p': p}}:
            gen = numeric.from_normal(n, p)
        case {'uniform': {'min': float() | int() as min, 'max': float() | int() as max}}:
            gen = numeric.from_uniform(min, max)
        case {'uniform': {'min': str() as min, 'max': str() as max, **rest}}:
            gen = dt.from_uniform(min, max, rest.get('format'))
        case {'range': {'start': float() | int() as start_, 'end': float() | int() as end_}}:
            gen = numeric.from_range(start_, end_)
        case {'range': {'start': str() as start_, 'end': str() as end_, **rest}}:
            gen = dt.from_range(start_, end_, rest.get('format'))
        case {'const': int() | float() as const}:
            gen = numeric.from_const(const)
        case {'const': str() as const}:
            gen = enum.from_enum([const])
        case {'enum': {'values': values}, **rest}:
            gen = enum.from_enum(values, rest.get('counts'), rest.get('shuffle') or False)
        case {'ref': (table, field)}:
            dep = generators[(table, field)]
            gen = lambda size: dep.sample(size, replace=True).reset_index(drop=True)
        case _:
            raise ValueError(f'Malformed Value: {val}')

    for f in val.get('filters') or ():
        match f:
            case {'add': arg}:
                match arg:
                    case {'const': int() | float() as const}:
                        gen = numeric.add(gen, const)
                    case dict():
                        gen = numeric.add(gen, get_generator(arg, generators))
            case {'subtract': arg}:
                match arg:
                    case {'const': int() | float() as const}:
                        gen = numeric.subtract(gen, const)
                    case dict():
                        gen = numeric.subtract(gen, get_generator(arg, generators))
            case {'subtract_from': arg}:
                match arg:
                    case {'const': int() | float() as const}:
                        gen = numeric.subtract_from(gen, const)
                    case dict():
                        gen = numeric.subtract_from(gen, get_generator(arg, generators))
            case {'multiply': arg}:
                match arg:
                    case {'const': int() | float() as const}:
                        gen = numeric.multiply(gen, const)
                    case dict():
                        gen = numeric.multiply(gen, get_generator(arg, generators))
            case {'floor': int() | float() as arg}:
                gen = numeric.floor(gen, arg)
            case {'ceiling': int() | float() as arg}:
                gen = numeric.ceiling(gen, arg)
            case {'round': int() as arg}:
                gen = numeric.round_(gen, arg)
            case _:
                raise ValueError(f'Malformed filter {f}')

    return gen
