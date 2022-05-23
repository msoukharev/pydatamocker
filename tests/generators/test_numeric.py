import pytest
from typing import cast
from pydatamocker.generators.numeric import from_numeric
from pydatamocker.types import FILTER_OPERATORS, NUMERIC_DISTRIBUTIONS, FieldParams
from tests.util import assert_elements_type, assert_match_regex, assert_nonempty, assert_series_superset


INTEGER_ARGUMENTS = {
    'n': 10,
    'p': 0.3,
    'min': 10,
    'max': 30,
    'start': 30,
    'end': 5000,
    'const': 20,
}


FLOAT_ARGUMENTS = {
    'mean': 10.3,
    'std': 3.1,
    'min': 10.1,
    'max': 30.3223,
    'start': 30.0,
    'end': 5000.2,
    'constr': -3.09
}


SAMPLE_SIZE = 180_000


def test_integer_distr():
    for distr in [d for d in NUMERIC_DISTRIBUTIONS if d != 'normal']:
        spec = {
            'type': 'number',
            'distr': {
                'name': distr,
                **INTEGER_ARGUMENTS
            }
        }
        sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty(sample)
        assert_elements_type(sample, int)


def test_float_distr():
    for distr in [d for d in NUMERIC_DISTRIBUTIONS if d != 'binomial']:
        spec = {
            'type': 'number',
            'distr': {
                'name': distr,
                **FLOAT_ARGUMENTS
            }
        }
        sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty(sample)
        assert_elements_type(sample, float)


def test_integer_const():
    spec = {
        'type': 'float',
        'const': 10
    }
    sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, int)
    for i in sample:
        assert i == 10, 'Wrong value instead of constant: {i}'


def test_float_const():
    spec = {
        'type': 'float',
        'const': 1.10
    }
    sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
    assert_elements_type(sample, float)
    for i in sample:
        assert i == 1.10, 'Wrong value instead of constant: {i}'


def test_filter_distr():
    for filter in ['add', 'subtract', 'subtract_from']:
        spec = {
            'type': 'number',
            'distr': {
                'name': 'binomial',
                **INTEGER_ARGUMENTS
            },
            'filters': [
                {
                    'operator': filter,
                    'argument': {
                        'type': 'number',
                        'distr': {
                            'name': 'range',
                            **FLOAT_ARGUMENTS
                        }
                    }
                }
            ]
        }
        sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty(sample)


def test_ceiling():
    for filter in ['ceiling']:
        spec = {
            'type': 'number',
            'const': 13412341,
            'filters': [
                {
                    'operator': filter,
                    'argument': {
                        'type': 'number',
                        'const': 10.2
                    }
                }
            ]
        }
        sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty(sample)
        assert_elements_type(sample, float)
        assert_series_superset(sample, [10.2])


def test_floor():
    for filter in ['floor']:
        spec = {
            'type': 'number',
            'const': -123.23,
            'filters': [
                {
                    'operator': filter,
                    'argument': {
                        'type': 'number',
                        'const': 10
                    }
                }
            ]
        }
        sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty(sample)
        assert_elements_type(sample, int)
        assert_series_superset(sample, [10])


def test_round():
    round = 2
    spec = {
        'type': 'number',
        'const': 103.389080342,
        'filters': [
            {
                'operator': 'round',
                'argument': {
                    'type': 'number',
                    'const': round
                }
            }
        ]
    }
    sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, float)
    assert_match_regex(sample, f'^\\d+\\.(\\d){{{round}}}$')


def test_round_integer():
    spec = {
        'type': 'number',
        'const': 103.389080342,
        'filters': [
            {
                'operator': 'round',
                'argument': {
                    'type': 'number',
                    'const': 0
                }
            }
        ]
    }
    sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, int)
    assert_match_regex(sample, f'^\\d+$')
