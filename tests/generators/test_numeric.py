import pytest
from pydatamocker.generators.numeric import generate
from ..asserts import assert_equals

PROPS = {
    'mean': 10,
    'std': 3,
    'n': 10,
    'p': 0.3,
    'min': 10,
    'max': 30,
    'start': 30,
    'end': 5000,
    'round': 4
}

MOCK_TYPE_TREE = {
    'float': {'uniform', 'normal', 'range'},
    'integer': {'uniform', 'binomial', 'range', 'normal'}
}

PROPS_MIN_CONFIGS = {
    'uniform': [
        {'min': -323 }, {'max': 9311}, {}
    ],
    'range': [
        {'start': -314}, {'end': 12323}, {}
    ]
}

SAMPLE_SIZE = 320030

def _assert_no_na(sample, type_, distr):
    assert_equals(0, sample.isna().sum(),
        f"NaN values are present in the series. Type: {type_}, Distribution: {distr}"
    )

def test_no_nans():
    for type_, distributions in MOCK_TYPE_TREE.items():
        for distr in distributions:
            sample = generate(**{**PROPS, 'distr': distr, 'datatype': type_, 'size': SAMPLE_SIZE, 'name': 'text'})
            _assert_no_na(sample, type_, distr)
