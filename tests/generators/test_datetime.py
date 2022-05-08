import pytest
from pydatamocker.generators.datetime import create
from ..asserts import assert_equals

VALUES = [
    {
        'distr': {
            'name': 'range',
            'start': '2019-02-20',
            'end': '2019-03-30',
        },
        'format': 'date'
    },
    {
        'distr': {
            'name': 'uniform',
            'start': '2019-02-28T11:30:00Z',
            'end': '2019-03-02T21:30:00Z'
        },
        'format': 'datetime'
    }
]

SAMPLE_SIZE = 25723

def test_no_nans():
    for val in VALUES:
        sample = create({ 'type': 'datetime', **val  })(SAMPLE_SIZE)  # type: ignore
        assert_equals(0, sample.isna().sum(),
            f"NaN values are present in the series. Distribution: {val['distr']['name']}."
        )
