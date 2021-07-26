from pandas import Series, DataFrame, concat
from .sampler import get_sample_generators
from .mocker import get_configs


def build_dataframe(fields_describe: dict, size: int) -> DataFrame:
    df = None
    report_progress = get_configs('report_progress')
    for field, field_spec in fields_describe['fields'].items():
        report_progress and print('Sampling', field, '...')
        sample = get_sample_generators(field, field_spec['mock_type'], **field_spec['props'])(size)
        if not type(sample) is Series:
            name = field
        else:
            name = sample.name or field
        df = concat([df, Series(sample, name=name)], axis=1)
    for lookup in fields_describe['lookups']:
        ldf = lookup['table'].get_dataframe()
        lookup_fields = lookup['fields']
        df = concat([ df, ldf[lookup_fields].sample(n=size, ignore_index=True, replace=True) ], axis=1)
    report_progress and print('Done!')
    return df
