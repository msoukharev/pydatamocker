from pandas import DataFrame
from multiprocessing import Pool
from pandas import Series, DataFrame
from .generators import factory

def _apply(props) -> Series:
    return factory(**props)(**props)

def build(size: int, table_spec: dict) -> DataFrame:
    samples = DataFrame()
    with Pool(6) as p:
        res = p.map(_apply, [
            {**field, 'name': name, 'size': size} for name, field in table_spec.items()
        ])
    for field_name, sample in zip(table_spec.keys(), res):
        samples[field_name] = sample
    return samples
