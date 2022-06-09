from pandas import Series
import pytest

from pydatamocker.core.field.string import append, prepend
from tests.util import assert_, eq, mismatch


def test_append():
    gen = lambda size: Series([1] * size)
    const = 'string'
    appended = append(gen, const)
    for val in appended(10):
        assert_(val, eq('1string'), mismatch('1string'))

def test_prepend():
    gen = lambda size: Series([1] * size)
    const = 'string'
    appended = prepend(gen, const)
    for val in appended(10):
        assert_(val, eq('string1'), mismatch('string1'))
