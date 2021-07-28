from pandas import Series, DataFrame, concat
from .mocker import get_configs
from .io import load_dataset, load_table, DATASETS
from .numbers import get_sample as num_sample, TYPES as NUMTYPES
from .time import get_sample as time_sample

def _table_column_sample(path: str, field_name: str, size: int):
    dataset = load_table(path)
    return dataset[field_name].sample(n=size, replace=True).reset_index(drop=True)


def get_sample(field_name: str, mock_type: str, size: int, **props):
    if mock_type in DATASETS:
        return load_dataset(mock_type).sample(n=size, ignore_index=True, replace=True)
    elif mock_type in NUMTYPES:
        return num_sample(mock_type, size, **props)
    elif mock_type == 'enum':
        return Series(props['values']).sample(n=size, ignore_index=True, replace=True, weights=props['weights'])
    elif mock_type in { 'date', 'datetime' }:
        return time_sample(mock_type, size, **props)
    elif mock_type == 'table':
        return _table_column_sample(props['path'], field_name, size)
    else:
        raise ValueError('Unsupported type')



def build_dataframe(fields_describe: dict, size: int) -> DataFrame:
    df = None
    report_progress = get_configs('report_progress')
    for field, field_spec in fields_describe['fields'].items():
        report_progress and print('Sampling', field, '...')
        sample = get_sample(field, field_spec['mock_type'], size, **field_spec['props'])
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
