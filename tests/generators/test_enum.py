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
        'distr': 'ordered'
    }
]

def test_sample_is_subset():
    for props in PROPS:
        props = dict(props)
        uniques_set = set(create(**props)(SAMPLE_SIZE).unique())
        vals = props['values']
        vals_set = set(vals)
        assert uniques_set.issubset(vals_set), \
            f"Unique values in the sample of choices {vals} are not the subset of the choices"

def test_no_weight():
    props = dict(PROPS[0])
    del props['weights']
    sample = create(**props)(SAMPLE_SIZE)
    assert_subset(sample.unique(), set(props['values']),
        'The sample values are not a subset of the specified options'
    )

def test_ordered():
    spec = dict(PROPS[2])
    sample = create(**spec)(SAMPLE_SIZE)
    act = ','.join(sample)
    sample.sort_values()
    exp = ','.join(sample)
    assert_equals(exp, act, 'Elements were not ordered')
