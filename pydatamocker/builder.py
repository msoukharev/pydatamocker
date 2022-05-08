from multiprocessing import Pool
from typing import Iterable, Tuple
from pandas import Series, DataFrame, concat
from psutil import cpu_count
from pydatamocker.types import FieldToken
from .generators import create


_ParallelBuilderFuncPayload = Tuple[int, FieldToken]


def _apply(payload: _ParallelBuilderFuncPayload) -> Series:
    size, token = payload
    generate = create(token['params'])
    series = generate(size)
    series.name = token['name']
    return series


def build(size: int, field_tokens: Iterable[FieldToken]) -> DataFrame:
    items = [(size, tok) for tok in field_tokens]
    if size >= 300_000 or cpu_count() > 3:
        with Pool(cpu_count() // 2) as p:

            res = p.map(_apply, items)
        return concat(res, axis=1)
    else:
        return concat([_apply(item) for item in items], axis=1)
