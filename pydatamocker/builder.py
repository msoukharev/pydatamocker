from pandas import Series, DataFrame, concat
from .sampler import get_sample_generator


def build_series(name: str, field_descriptor: dict, size: int):
    get_sample = get_sample_generator(field_descriptor['mock_type'], **field_descriptor['props'])
    return Series(data=get_sample(size), name=name)


def build_dataframe(fields_describe: dict, size: int) -> DataFrame:
    fields_spec = fields_describe['fields']
    return concat([ build_series(name, fields_spec[name], size) for name in fields_spec.keys() ], axis=1)
