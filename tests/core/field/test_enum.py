from pydatamocker.core.field.enum import from_enum
from tests.util import assert_nonempty, assert_series_superset, assert_unique_count


SAMPLE_SIZE = 100_000


def test_enum():
    sample = from_enum(['a', 'b', 'c'], [1, 2, 3])(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_series_superset(sample, ['a', 'b', 'c'])
    assert_unique_count(sample, 3)


def test_no_weight():
    sample = from_enum(['a', 'b', 'c'])(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_unique_count(sample, 3)


def test_ordered():
    sample = from_enum(['a', 'b', 'c'], [1, 2, 3], shuffle=False)(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_series_superset(sample, ['a', 'b', 'c'])
    assert_unique_count(sample, 3)
