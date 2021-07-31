import pytest
from pydatamocker.choices import get_sample


SAMPLE_SIZE = 320030


PROPS = [
    {
        'values': [1, 9, 5, 6, 7, -1, 19],
        'weights': [3, 5, 6, 7, 3, 2, 10]
    },
    {
        'values': ['Rick', 'Morty', 'plumbus', 'CONSTANT'],
        'weights': [0.3, 0.2, 0.2, 0.1]
    }
]


def test_is_subset():
    for props in PROPS:
        uniques_set = set(get_sample(SAMPLE_SIZE, **props).unique())
        vals = props['values']
        vals_set = set(vals)
        assert uniques_set.issubset(vals_set), f"Unique values in the sample of choices {vals} are not the subset of the choices"
