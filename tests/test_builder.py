import pytest
from pydatamocker.builder import build
from .asserts import assert_equals
from pandas import DataFrame

SPEC = {
    'FirstName': {
        'dataset': 'first_name'
    },
    'Age': {
        'datatype': 'integer',
        'distr': 'binomial',
        'n': 40,
        'p': 0.7
    },
}

SAMPLE_SIZE = 1000

def test_build():
    res = build(SAMPLE_SIZE, SPEC)
    assert isinstance(res, (DataFrame)), "DataFrame type was not returned"
    assert 2 == len(res.columns), "Wrong number of columns"
    for name in SPEC.keys():
        assert name in set(res.columns), "Column missing " + name
    assert 1000 == len(res)
