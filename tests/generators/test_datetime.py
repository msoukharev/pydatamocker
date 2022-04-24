import pytest
from pydatamocker.generators.datetime import generate
from ..asserts import assert_equals

PROPS = {
    'date': {
        'name': 'test',
        'start': '2019-02-20',
        'end': '2019-03-30'
    },
    'datetime': {
        'name': 'test',
        'start': '2019-02-28T11:30:00Z',
        'end': '2019-03-02T21:30:00Z'
    }
}

MOCK_TYPE_TREE = {
    'date': { 'uniform', 'range' },
    'datetime': { 'uniform', 'range' }
}

SAMPLE_SIZE = 25723

def test_no_nans():
    for type_, distributions in MOCK_TYPE_TREE.items():
        for distr in distributions:
            sample = generate(
                **{ **PROPS[type_], 'distr': distr, 'datatype': type_, 'size': SAMPLE_SIZE }
            )
            assert_equals(0, sample.isna().sum(),
                f"NaN values are present in the series. Type: {type_}, Distribution: {distr}"
            )
