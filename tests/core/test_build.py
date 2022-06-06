from typing import List
import pytest
from pydatamocker.core.build import build
from pydatamocker.types import FieldBuildRequest
from tests.util import assert_, assert_nonempty, eq, mismatch


no_ref = [
    (10, { 'name': ('A', '1'), 'value': { 'const': 10} }),
    (10, { 'name': ('A', '2'), 'value': { 'const': 10} }),
    (20, { 'name': ('B', '1'), 'value': { 'const': 30} })
]

ref = [
    (10, { 'name': ('A', '1'), 'value': { 'const': 89 } }),
    (10, { 'name': ('A', '2'), 'value': { 'const': 10 } }),
    (30, { 'name': ('B', '1'), 'value': { 'ref': ('A', '1'), 'filters': [{ 'add': { 'ref': ('A', '2') } }] } }),
    (30, { 'name': ('B', '2'), 'value': { 'const': 10032 } })
]

cycle: List[FieldBuildRequest] = [
    (10, { 'name': ('A', '1'), 'value': { 'const': 80 } }),
    (10, { 'name': ('A', '2'), 'value': { 'ref': ('A', '3') } }),
    (10, { 'name': ('A', '3'), 'value': { 'ref': ('A', '2') } })
]


def test_no_ref():
    results = build(no_ref)
    assert_(len(results), eq(3), mismatch(3))
    for _, ser in results:
        assert_nonempty(ser)


def test_ref():
    results = build(ref)
    assert_(len(results), eq(4), mismatch(4))
    for _, ser in results:
        assert_nonempty(ser)


def test_cycle():
    try:
        res = build(cycle)
    except:
        return
    assert False, 'No exception was raised'
