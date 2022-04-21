import pytest
from pydatamocker.table import createEmpty, createFromConfig, createFromJSON
from tempfile import TemporaryFile
import os

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

CONFIG = {
    'title': 'TestTable',
    'fields': FIELDS_SPEC
}

TESTCONFIG_PATH = os.path.abspath(os.path.join(__file__, os.pardir, 'data', 'testconfig.json'))

def _assert_table(table):
    res = table.sample(SAMPLE_SIZE)
    assert SAMPLE_SIZE == len(res), 'Wrong number of records'
    assert len(FIELDS_SPEC) == len(res.columns)
    for name in FIELDS_SPEC.keys():
        assert name in set(res.columns), 'Column missing: ' + name

def test_createEmpty():
    tab = createEmpty('Test')
    for name, spec in FIELDS_SPEC.items():
        tab.field(name, **spec)
    _assert_table(tab)

def test_createFromConfig():
    tab = createFromConfig(CONFIG)
    _assert_table(tab)

def test_createFromJSON():
    tab = createFromJSON(TESTCONFIG_PATH)
    _assert_table(tab)

def test_sampleWithConfigSize():
    conf = { ** CONFIG, 'size': 70 }
    tab = createFromConfig(conf)
    assert 70 == len(tab.sample()), 'Specified size was not read from the config'

def test_reorderFields():
    tab = createFromConfig(CONFIG)
    expectedorder = ['FormStatus', 'LastName', 'FirstName', 'Age', 'Bucket', 'Registered', 'LastLogin']
    tab.reorderFields(expectedorder[:3])
    exp = ';'.join(expectedorder)
    act = ';'.join(tab.config['fields'].keys())
    assert exp == act, 'Wrong order for fields in the config'
