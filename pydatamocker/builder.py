from pandas import DataFrame
from multiprocessing import Pool
from pandas import Series, DataFrame
from .generators import factory

def _apply(props) -> Series:
    return factory(**props)(**props)

def build(size: int, field_specs: dict) -> DataFrame:
    samples = DataFrame()
    if size >= 100_000:
        with Pool(6) as p:
            res = p.map(_apply, [
                {**field, 'name': name, 'size': size} for name, field in field_specs.items()
            ])
        for field_name, sample in zip(field_specs.keys(), res):
            samples[field_name] = sample
    else:
        for field_name, field_spec in field_specs.items():
            samples[field_name] = _apply({ **field_spec, 'size': size })
    return samples
