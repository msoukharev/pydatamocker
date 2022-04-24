from multiprocessing import Pool
from typing import Iterable
from pandas import Series, DataFrame, concat
from .generators import factory

def _apply(props) -> Series:
    return factory(**props)(**props)

def build(size: int, field_specs: Iterable) -> DataFrame:
    if size >= 100_000:
        with Pool(6) as p:
            res = p.map(_apply, [
                {**field, 'size': size} for field in field_specs
            ])
        return concat(res, axis=1)
    else:
        return concat([_apply({ **spec, 'size': size }) for spec in field_specs], axis=1)
