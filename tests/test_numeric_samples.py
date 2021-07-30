import pytest
from pydatamocker.numbers import get_sample


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
            assert sample.isna().sum() == 0, f"NaN values are present in the series. Type: {type_}, Distribution: {distr}"
