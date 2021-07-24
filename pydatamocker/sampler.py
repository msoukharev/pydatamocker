from pandas.core.frame import DataFrame
from .io import load_dataset, load_table, DATASETS
from pandas import Series
from .numbers import get_distribution_sampler, TYPES as NUMTYPES
from .time import get_chrono_sampler


def _dataset_sample_generators(mock_type):
    return lambda size: (load_dataset(mock_type).sample(n=size, ignore_index=True, replace=True) for _ in [0])


def _numberic_sample_generators(mock_type: str, **props):
    distr = props.pop('distr')
    return lambda size: (get_distribution_sampler(mock_type, distr, **props)(size) for _ in [0])


def _enum_sample_generators(**props):
    values = props.pop('values')
    weights = props.pop('weights') if 'weights' in props else None
    return lambda size: (Series(values).sample(n=size, ignore_index=True, replace=True, weights=weights) for _ in [0])


def _chrono_sample_generators(mock_type: str, **props):
    distr = props.pop('distr')
    return lambda size: (get_chrono_sampler(mock_type, distr, **props)(size) for _ in [0])


def _multicolumn_sampler(dataset, size, columns):
    sample = dataset.sample(n=size, replace=True).reset_index(drop=True)
    return [sample[col] for col in columns]


def _table_data_generators(path: str):
    dataset = load_table(path)
    columns = dataset.columns
    return lambda size: _multicolumn_sampler(dataset, size, columns)


def get_sample_generators(mock_type: str, **props):
    if mock_type in DATASETS:
        return _dataset_sample_generators(mock_type)
    elif mock_type in NUMTYPES:
        return _numberic_sample_generators(mock_type, **props)
    elif mock_type == 'enum':
        return _enum_sample_generators(**props)
    elif mock_type in { 'date', 'datetime' }:
        return _chrono_sample_generators(mock_type, **props)
    elif mock_type == 'table' and props.get('path'):
        path = props.pop('path')
        return _table_data_generators(path)
    else:
        raise ValueError('Unsupported type')
