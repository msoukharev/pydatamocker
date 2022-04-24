import pytest
from pydatamocker.table import Table, createEmpty, createFromConfig, createFromJSON
import os
from tests.asserts import assert_equals
import json


SAMPLE_SIZE = 1_000

def load_spec() -> dict:
    with open(os.path.join(os.path.dirname(__file__), 'data', 'testconfig.json'), 'r') as f:
        return json.load(f)

FIELDS_SPEC = load_spec()['fields']

CONFIG = {
    'title': 'TestTable',
    'fields': FIELDS_SPEC
}

TESTCONFIG_PATH = os.path.abspath(os.path.join(__file__, os.pardir, 'data', 'testconfig.json'))

def _assert_table(table: Table):
    res = table.sample(SAMPLE_SIZE)
    assert SAMPLE_SIZE == len(res), 'Wrong number of records'
    assert len(FIELDS_SPEC) == len(res.columns)
    for field in FIELDS_SPEC:
        assert field['name'] in set(res.columns), 'Column missing: ' + field['name']

def test_createEmpty():
    tab = createEmpty('Test')
    for spec in FIELDS_SPEC:
        tab.field(**spec)
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
    assert_equals(70, len(tab.sample()), 'Specified size was not read from the config')

def test_no_title():
    invalid = dict(CONFIG)
    del invalid['title']
    try:
        _ = createFromConfig(invalid)
    except ValueError as _:
        return
    assert False, 'No exception raised'


def test_no_size():
    try:
        tab = createFromConfig(CONFIG)
        tab.sample()
    except ValueError as _:
        return
    assert False, 'No exception raised'
