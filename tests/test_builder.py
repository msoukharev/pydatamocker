import pytest
from pydatamocker.builder import build
from pandas import DataFrame
import json
import os


def load_spec() -> dict:
    with open(os.path.join(os.path.dirname(__file__), 'data', 'testconfig.json'), 'r') as f:
        return json.load(f)


FIELDS_SPEC = load_spec()['fields']


SAMPLE_SIZE = 100_000


def test_build():
    res = build(SAMPLE_SIZE, FIELDS_SPEC)
    assert isinstance(res, (DataFrame)), "DataFrame type was not returned"
    assert len(FIELDS_SPEC) == len(res.columns), "Wrong number of columns"
    for spec in FIELDS_SPEC:
        assert spec['name'] in set(res.columns), "Column missing " + spec['name']
    assert SAMPLE_SIZE == len(res)
