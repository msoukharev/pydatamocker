import pytest
from typing import cast
from pydatamocker.generators.numeric import from_numeric
from pydatamocker.types import FILTER_OPERATORS, FLOAT_DISTRIBUTIONS, INTEGER_DISTRIBUTIONS, FieldParams
from tests.util import assert_elements_type, assert_nonempty


INTEGER_ARGUMENTS = {
    'mean': 10,
    'std': 3,
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
    for distr in INTEGER_DISTRIBUTIONS:
        spec = {
            'type': 'integer',
            'distr': {
                'name': distr,
                **INTEGER_ARGUMENTS
            }
        }
        sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty(sample)
        assert_elements_type(sample, int)


def test_float_distr():
    for distr in FLOAT_DISTRIBUTIONS:
        spec = {
            'type': 'float',
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


def test_integer_filter():
    for filter in FILTER_OPERATORS:
        spec = {
            'type': 'integer',
            'distr': {
                'name': INTEGER_DISTRIBUTIONS[0],
                **INTEGER_ARGUMENTS
            },
            'filters': [
                {
                    'operator': filter,
                    'argument': {
                        'type': 'integer',
                        'distr': {
                            'name': INTEGER_DISTRIBUTIONS[0],
                            **INTEGER_ARGUMENTS
                        },
                        'const': 10
                    }
                }
            ]
        }
        sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty(sample)


def test_float_filter():
    for filter in FILTER_OPERATORS:
        spec = {
            'type': 'integer',
            'distr': {
                'name': FLOAT_DISTRIBUTIONS[0],
                **FLOAT_ARGUMENTS
            },
            'filters': [
                {
                    'operator': filter,
                    'argument': {
                        'type': 'integer',
                        'distr': {
                            'name': FLOAT_DISTRIBUTIONS[0],
                            **FLOAT_ARGUMENTS
                        },
                        'const': 10.12
                    }
                }
            ]
        }
        sample = from_numeric(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty(sample)
