import pytest
from pydatamocker.types.number import get_sample
from .asserts import assert_equals


PROPS = {
    'mean': 10,
    'std': 3,
    'n': 10,
    'p': 0.3,
    'min': 10,
    'max': 30,
    'start': 30,
    'end': 5000
}


MOCK_TYPE_TREE = {
    'float': { 'uniform', 'normal', 'range' },
    'integer': { 'uniform', 'binomial', 'range' }
}


SAMPLE_SIZE = 320030


def test_no_nans():
    for type_, distributions in MOCK_TYPE_TREE.items():
        for distr in distributions:
            sample = get_sample(type_, SAMPLE_SIZE, **{ **PROPS, 'distr': distr})
            assert_equals(0, sample.isna().sum(), f"NaN values are present in the series. Type: {type_}, Distribution: {distr}")
