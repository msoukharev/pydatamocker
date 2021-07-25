from .io import load_dataset, load_table, DATASETS
from pandas import Series
from .numbers import get_sample as num_sample, TYPES as NUMTYPES
from .time import get_sample as time_sample


def _multicolumn_sampler(dataset, size, columns):
    sample = dataset.sample(n=size, replace=True).reset_index(drop=True)
    return [sample[col] for col in columns]


def _table_data_generators(path: str):
    dataset = load_table(path)
    columns = dataset.columns
    return lambda size: _multicolumn_sampler(dataset, size, columns)


def get_sample_generators(mock_type: str, **props):
    if mock_type in DATASETS:
        return lambda size: (load_dataset(mock_type).sample(n=size, ignore_index=True, replace=True) for _ in [0])
    elif mock_type in NUMTYPES:
        return lambda size: (num_sample(mock_type, size, **props) for _ in [0])
    elif mock_type == 'enum':
        return lambda size: (Series(props['values']).sample(n=size, ignore_index=True, replace=True, weights=props['weights'])
            for _ in [0])
    elif mock_type in { 'date', 'datetime' }:
        return lambda size: (time_sample(mock_type, size, **props) for _ in [0])
    elif mock_type == 'table' and props.get('path'):
        path = props.pop('path')
        return _table_data_generators(path)
    else:
        raise ValueError('Unsupported type')
