from typing import Any, Tuple, Dict
from pandas import Series
from pydatamocker.core.field.factory import get_generator
from pydatamocker.types import Value
from tests.util import assert_all, assert_nonempty, eq, mismatch


vals = [
    {
        'dataset': {
            'name': 'first_name'
        }
    },
    {
        'normal': {
            'mean': 10,
            'std': 3
        }
    },
    {
        'binomial': {
            'n': 103,
            'p': 321
        }
    },
    {
        'uniform': {
            'min': 1,
            'max' :123213
        }
    },
    {
        'range': {
            'start': 23,
            'end': 290.23
        }
    },
    {
        'const': -23.23
    },
    {
        'const': 10
    },
    {
        'const': 'TestValue'
    },
    {
        'enum': {
            'values': ['a', 'b', 'c'],
            'counts': [1, 3, 4]
        }
    },
    {
        'range': {
            'start': '2021-02-13',
            'end': '2039-11-11',
            'format': 'datetime'
        }
    },
    {
        'uniform': {
            'min': '2021-02-13',
            'max': '2021-02-13'
        }
    }
]

invalid = [
    {
        'gloggalab': {
            'shlabble': 'dabble'
        }
    },
    {
        'normal': {
            'mean': 123,
            'n': 15
        }
    }
]

with_filter: Tuple[Value, Any] = ({
    'const': 102,
    'filters': [
        {
            'add': {
                'const': 23
            }
        },
        {
            'subtract': {
                'const': 90
            }
        },
        {
            'subtract_from': {
                'const': 1232
            }
        },
        {
            'multiply': {
                'const': 90.3
            }
        },
    ]
}, (1232 - (102 + 23 - 90)) * 90.3)


def test_get_generator():
    for val in vals:
        gen = get_generator(val, {})
        sample = gen(10)
        assert_nonempty(sample)


def test_raise_invalid():
    for val in invalid:
        try:
            _ = get_generator(val)
        except ValueError:
            continue
        assert False, 'ValueError was not raised'


def test_with_filter():
    gen = get_generator(with_filter[0])
    sample = gen(12323)
    assert_nonempty(sample)
    assert_all(sample, lambda el: el == with_filter[1], lambda el: f'Expected {with_filter[1]} got {el}')


def test_ref():
    val: Value = {
        'ref': ('A', '1' ),
        'filters':[
            {
                'add': {
                    'ref': ('B', '2')
                }
            }
        ]
    }
    sample = get_generator(val, {
        ('A', '1'): Series([5] * 10),
        ('B', '2'): Series([98] * 10),
    })(10)
    assert_nonempty(sample)
    assert_all(sample, eq(5 + 98), mismatch(5 + 98))


def test_ref_missing():
    val: Value = {
        'ref': ('A', '1'),
        'filters':[
            {
                'add': {
                    'ref': ('B', '2')
                }
            }
        ]
    }
    try:
        _ = get_generator(val, {
            ('A', '1'): Series(100),
            ('C', '3'): Series(100)
        })(100)
    except KeyError as _:
        return
    assert False, 'Exception was not raised'
