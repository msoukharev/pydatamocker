from multiprocessing import Pool
from typing import Any, Iterable
from pandas import Series, DataFrame, concat
from psutil import cpu_count
from .generators import create


def _apply(props: Any) -> Series:
    generate = create(**props)
    series = generate(props['size'])
    series.name = props['name']
    return series


def build(size: int, field_specs: Iterable) -> DataFrame:
    if size >= 300_000 or cpu_count() > 3:
        with Pool(cpu_count() // 2) as p:
            res = p.map(_apply, [
                {**field, 'size': size} for field in field_specs
            ])
        return concat(res, axis=1)
    else:
        return concat([_apply({ **spec, 'size': size }) for spec in field_specs], axis=1)
