import pytest
from typing import cast
from pydatamocker.generators.numeric import create
from pydatamocker.types import FLOAT_DISTRIBUTIONS, INTEGER_DISTRIBUTIONS, FieldParams
from tests.util import assert_nonempty_series


INTEGER_ARGUMENTS = {
    'mean': 10,
    'std': 3,
    'n': 10,
    'p': 0.3,
    'min': 10,
    'max': 30,
    'start': 30,
    'end': 5000,
}


FLOAT_ARGUMENTS = {
    'mean': 10.3,
    'std': 3.1,
    'min': 10.1,
    'max': 30.3223,
    'start': 30.0,
    'end': 5000.2
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
        sample = create(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty_series(sample)


def test_float_distr():
    for distr in FLOAT_DISTRIBUTIONS:
        spec = {
            'type': 'float',
            'distr': {
                'name': distr,
                **FLOAT_ARGUMENTS
            }
        }
        sample = create(cast(FieldParams, spec))(SAMPLE_SIZE)
        assert_nonempty_series(sample)
