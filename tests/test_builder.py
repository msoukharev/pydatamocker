import pytest
from pydatamocker.builder import build
from pandas import DataFrame

from pydatamocker.exceptions.builder import BuilderException

FIELDS_SPEC = {
    'FirstName': {
        'dataset': 'first_name'
    },
    'LastName': {
        'dataset': 'last_name'
    },
    'Age': {
        'datatype': 'integer',
        'distr': 'binomial',
        'n': 40,
        'p': 0.7
    },
    'FormStatus': {
        'datatype': 'enum',
        'values': ['Overdue', 'Pending', 'Completed'],
        'weights': [2, 8, 90]
    },
    'Bucket': {
        'datatype': 'enum',
        'values': ['1', '2', '3']
    },
    'Registered': {
        'datatype': 'date',
        'distr': 'range',
        'start': '2018-02-13',
        'end': '2020-10-30'
    },
    'LastLogin': {
        'datatype': 'datetime',
        'distr': 'range',
        'start': '2020-09-23T10:10:30',
        'end': '2022-03-23T20:20:00'
    }
}

SAMPLE_SIZE = 1_000_000

def test_build():
    res = build(SAMPLE_SIZE, FIELDS_SPEC)
    assert isinstance(res, (DataFrame)), "DataFrame type was not returned"
    assert len(FIELDS_SPEC) == len(res.columns), "Wrong number of columns"
    for name in FIELDS_SPEC.keys():
        assert name in set(res.columns), "Column missing " + name
    assert SAMPLE_SIZE == len(res)

def test_raise_dataset_datatype():
    invalid = dict(FIELDS_SPEC)
    invalid['FakeField'] = {
        'dataset': 'a',
        'datatype': 'b'
    }
    try:
        build(SAMPLE_SIZE, invalid)
    except ValueError as _:
        return
    assert False, 'No exception raised'
