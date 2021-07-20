from ..io.loader import load_dataset, DATASETS
from pandas import Series
from .numeric import get_distribution_sampler, RANDOM_TYPES
from .chrono import get_chrono_sampler


def _loaded_series_sample_generator(mock_type):
    return lambda size: load_dataset(mock_type).sample(n=size, ignore_index=True, replace=True)


def _random_set_generator(mock_type: str, **props):
    distr = props.pop('distr')
    return get_distribution_sampler(mock_type, distr, **props)


def _enum_random_generator(**props):
    values = props.pop('values')
    weights = props.pop('weights') if 'weights' in props else None
    return lambda size: Series(values).sample(n=size, ignore_index=True, replace=True, weights=weights)


def _chrono_random_generator(mock_type: str, **props):
    distr = props.pop('distr')
    return get_chrono_sampler(mock_type, distr, **props)


def get_sample_generator(mock_type: str, **props):
    if mock_type in DATASETS:
        return _loaded_series_sample_generator(mock_type)
    elif mock_type in RANDOM_TYPES:
        return _random_set_generator(mock_type, **props)
    elif mock_type == 'enum':
        return _enum_random_generator(**props)
    elif mock_type in { 'date', 'datetime' }:
        return _chrono_random_generator(mock_type, **props)
    else:
        raise ValueError('Unsupported type')
