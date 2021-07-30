from pandas import Series, DataFrame, concat
from .mocker import get_config
from .io import get_dataset_sample, get_table_sample, DATASETS
from .numbers import get_sample as num_sample, TYPES as NUMTYPES
from .time import get_sample as time_sample


class _SampleCache:

    def __init__(self) -> None:
        self.data = {}

    def get_sample(self, mock_table, size: int):
        sample = self.data.get(mock_table.name)
        if sample is None or len(sample) != size:
            sample = mock_table.get_dataframe().sample(n=size, replace=True).reset_index(drop=True)
            self.data[mock_table.name] = sample
        return sample


_sample_cache = _SampleCache()


def get_sample(field_name: str, mock_type: str, size: int, **props):
    if mock_type in DATASETS:
        return get_dataset_sample(mock_type, size)
    elif mock_type in NUMTYPES:
        return num_sample(mock_type, size, **props)
    elif mock_type == 'enum':
        return Series(props['values']).sample(n=size, replace=True, weights=props['weights']).reset_index(drop=True)
    elif mock_type in { 'date', 'datetime' }:
        return time_sample(mock_type, size, **props)
    elif mock_type == 'table':
        return get_table_sample(props['path'], field_name, size)
    elif mock_type == 'mock_reference':
        return _sample_cache.get_sample(props['mock_table'], size)[field_name]
    else:
        raise ValueError('Unsupported type')


def build_dataframe(fields_describe: dict, size: int) -> DataFrame:
    df = None
    report_progress = get_config('report_progress')
    for field, field_spec in fields_describe['fields'].items():
        report_progress and print('Sampling', field, '...')
        sample = get_sample(field, field_spec['mock_type'], size, **field_spec['props'])
        sample.name = sample.name or field
        df = concat([df, sample], axis=1)
    report_progress and print('Done!')
    return df
