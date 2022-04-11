import pytest
from pydatamocker.generators.enum import *
from ..asserts import assert_subset

SAMPLE_SIZE = 500_000

PROPS = [
    {
        'values': [1, 9, 5, 6, 7, -1, 19],
        'weights': [3, 5, 6, 7, 3, 2, 10]
    },
    {
        'values': ['New', 'Deprecated', 'Retired'],
        'weights': [0.3, 0.2, 0.2]
    },
    {
        'values': ['New', 'Deprecated', 'Retired'],
        'weights': [0.3, 0.2, 0.2],
        'distr': 'ordered'
    }
]

def test_sample_is_subset():
    for props in PROPS:
        uniques_set = set(generate(SAMPLE_SIZE, **props).unique())
        vals = props['values']
        vals_set = set(vals)
        assert uniques_set.issubset(vals_set), \
            f"Unique values in the sample of choices {vals} are not the subset of the choices"

def test_no_weight():
    props = dict(PROPS[0])
    del props['weights']
    sample = generate(SAMPLE_SIZE, **props)
    assert_subset(sample.unique(), set(props['values']),
        'The sample values are not a subset of the specified options'
    )

def test_ordered():
    spec = PROPS[2]
    sample = generate(300, **spec)
    act = ','.join(sample)
    sample.sort_values()
    exp = ','.join(sample)
    assert exp == act, 'Elements were not ordered'
