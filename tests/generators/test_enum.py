from pydatamocker.generators.enum import *
from tests.util import assert_nonempty_series, assert_series_superset
from ..asserts import assert_equals


SAMPLE_SIZE = 5_000


PARAMS: Iterable[FieldParams] = [
    {
        'type': 'enum',
        'distr': {
            'values': [1, 9, 5, 6, 7, -1, 19],
            'weights': [3, 5, 6, 7, 3, 2, 10]
        }
    },
    {
        'type': 'enum',
        'distr': {
            'values': ['New', 'Deprecated', 'Retired'],
            'weights': [0.3, 0.2, 0.2]
        }
    },
    {
        'type': 'enum',
        'distr': {
            'values': ['New', 'Deprecated', 'Retired'],
            'weights': [0.3, 0.2, 0.2],
            'name': 'ordered'
        }
    }
]

def test_enum():
    for param in PARAMS:
        sample = create(param)(SAMPLE_SIZE)
        assert_nonempty_series(sample)
        assert_series_superset(sample, param['distr']['values'])

def test_no_weight():
    params: FieldParams = PARAMS[0]
    del params['distr']['weights']
    sample = create(params)(SAMPLE_SIZE)
    assert_nonempty_series(sample)
    assert_series_superset(sample, params['distr']['values'])

def test_ordered():
    spec = PARAMS[2]
    sample = create(spec)(SAMPLE_SIZE)
    act = ','.join(sample)
    sample.sort_values()
    exp = ','.join(sample)
    assert_equals(exp, act, 'Elements were not ordered')
