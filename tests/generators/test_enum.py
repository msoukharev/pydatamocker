import pytest
from pydatamocker.generators.enum import *
from ..asserts import assert_equals, assert_subset

SAMPLE_SIZE = 500_000

PROPS = [
    {
        'name': 'test',
        'values': [1, 9, 5, 6, 7, -1, 19],
        'weights': [3, 5, 6, 7, 3, 2, 10]
    },
    {
        'name': 'test',
        'values': ['New', 'Deprecated', 'Retired'],
        'weights': [0.3, 0.2, 0.2]
    },
    {
        'name': 'test',
        'values': ['New', 'Deprecated', 'Retired'],
        'weights': [0.3, 0.2, 0.2],
        'distr': 'order'
    }
]

def test_sample_is_subset():
    for props in PROPS:
        props = dict(props)
        props['size'] = SAMPLE_SIZE
        uniques_set = set(generate(**props).unique())
        vals = props['values']
        vals_set = set(vals)
        assert uniques_set.issubset(vals_set), \
            f"Unique values in the sample of choices {vals} are not the subset of the choices"

def test_no_weight():
    props = dict(PROPS[0])
    del props['weights']
    props['size'] = SAMPLE_SIZE
    sample = generate(**props)
    assert_subset(sample.unique(), set(props['values']),
        'The sample values are not a subset of the specified options'
    )

def test_ordered():
    spec = dict(PROPS[2])
    spec['size'] = SAMPLE_SIZE
    sample = generate(**spec)
    act = ','.join(sample)
    sample.sort_values()
    exp = ','.join(sample)
    assert_equals(exp, act, 'Elements were not ordered')
