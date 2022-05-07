import pytest
from pydatamocker.generators.enum import *
from tests.util import assert_nonempty_series, assert_series_superset
from ..asserts import assert_equals


SAMPLE_SIZE = 5_000


SPECS: Iterable[EnumFieldSpec] = [
    {
        'type': 'enum',
        'value': {
            'values': [1, 9, 5, 6, 7, -1, 19],
            'weights': [3, 5, 6, 7, 3, 2, 10]
        }
    },
    {
        'type': 'enum',
        'value': {
            'values': ['New', 'Deprecated', 'Retired'],
            'weights': [0.3, 0.2, 0.2]
        }
    },
    {
        'type': 'enum',
        'value': {
            'values': ['New', 'Deprecated', 'Retired'],
            'weights': [0.3, 0.2, 0.2],
            'distr': 'ordered'
        }
    }
]

def test_enum():
    for spec in SPECS:
        sample = create(spec)(SAMPLE_SIZE)
        assert_nonempty_series(sample)
        assert_series_superset(sample, spec['value']['values'])

def test_no_weight():
    spec: EnumFieldSpec = SPECS[0]
    del spec['value']['weights']
    sample = create(spec)(SAMPLE_SIZE)
    assert_nonempty_series(sample)
    assert_series_superset(sample, spec['value']['values'])

def test_ordered():
    spec = SPECS[2]
    sample = create(spec)(SAMPLE_SIZE)
    act = ','.join(sample)
    sample.sort_values()
    exp = ','.join(sample)
    assert_equals(exp, act, 'Elements were not ordered')
