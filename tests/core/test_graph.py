import pytest
from typing import List
from pydatamocker.types import Field
from pydatamocker.core.graph import graph
from tests.util import assert_, eq, mismatch


acyclic: List[Field] = [
    {
        'name': ('A', '1'),
        'value': {}
    },
    {
        'name': ('A', '2'),
        'value': { 'ref': ('A', '1') }
    },
    {
        'name': ('A', '3'),
        'value': { 'ref': ('A', '1'), 'filters': [
                {
                    'add': {
                        'ref': ('A', '2')
                    }
                }
            ]
        }
    },
    {
        'name': ('A', '4'),
        'value': {}
    }
]


no_entry: List[Field] = [
    {
        'name': ('A', '1'),
        'value': {
            'const': 10, 'filters': [
                {
                    'add': {
                        'ref': ('A', '1')
                    }
                }
            ]
        }
    },
    {
        'name': ('A', '2'),
        'value': {
            'ref': ('A', '1'),
            'filters': [
                {
                    'add': {
                        'ref': ('A', '3')
                    }
                }
            ]
        }
    },
    {
        'name': ('A', '3'),
        'value': {
            'ref': ('A', '1')
        }
    }
]


def test_acyclic():
    build_order = list(graph(acyclic))
    assert_(len(build_order), eq(3), mismatch(3))
    subjects = [
        {('A', '1'), ('A', '4')},
        {('A', '2')},
        {('A', '3')}
    ]
    for i, expected_set in enumerate(subjects):
        act = set(build_order[i])
        assert_(act, eq(expected_set), mismatch(expected_set))


def test_no_entry():
    try:
        _ = list(graph(no_entry))
    except ValueError as _:
        return
    assert False, 'Error was not raised'
