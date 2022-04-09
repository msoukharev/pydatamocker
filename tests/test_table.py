import pytest
from pydatamocker.table import create, createByLoading, Table
from tempfile import TemporaryFile
# from .asserts import assert_equals

SAMPLE_SIZE = 1_000

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

def test_table():
    tab = create('Test')
    for name, spec in FIELDS_SPEC.items():
        tab.field(name, **spec)
    res = tab.sample(SAMPLE_SIZE)
    assert SAMPLE_SIZE == len(res), "Wrong number of records"
    assert len(FIELDS_SPEC) == len(res.columns)
    for name in FIELDS_SPEC.keys():
        assert name in set(res.columns), "Column missing: " + name
