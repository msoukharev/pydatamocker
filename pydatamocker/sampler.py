from .io import load_dataset, DATASETS
from pandas import Series
from .numbers import get_distribution_sampler, TYPES as NUMTYPES
from .time import get_chrono_sampler


def _dataset_sample_generator(mock_type):
    return lambda size: load_dataset(mock_type).sample(n=size, ignore_index=True, replace=True)


def _numberic_sample_generator(mock_type: str, **props):
    distr = props.pop('distr')
    return get_distribution_sampler(mock_type, distr, **props)


def _enum_sample_generator(**props):
    values = props.pop('values')
    weights = props.pop('weights') if 'weights' in props else None
    return lambda size: Series(values).sample(n=size, ignore_index=True, replace=True, weights=weights)


def _chrono_sample_generator(mock_type: str, **props):
    distr = props.pop('distr')
    return get_chrono_sampler(mock_type, distr, **props)


def get_sample_generator(mock_type: str, **props):
    if mock_type in DATASETS:
        return _dataset_sample_generator(mock_type)
    elif mock_type in NUMTYPES:
        return _numberic_sample_generator(mock_type, **props)
    elif mock_type == 'enum':
        return _enum_sample_generator(**props)
    elif mock_type in { 'date', 'datetime' }:
        return _chrono_sample_generator(mock_type, **props)
    else:
        raise ValueError('Unsupported type')
