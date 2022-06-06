import pytest
from pydatamocker.core.field.numeric import *
from tests.util import assert_all, assert_elements_type, assert_nonempty, assert_series_superset, assert_unique_count


SAMPLE_SIZE = 180_000


def test_binomial():
    sample = from_binomial(10, 0.3)(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, int)


def test_normal():
    sample = from_normal(1.2, 2.2)(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, float)


def test_uniform_integer():
    sample = from_uniform(10, 32)(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, int)


def test_uniform_float():
    sample = from_uniform(10, 32.9)(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, float)


def test_range_integer():
    for mi, ma in [(1, 20), (1, SAMPLE_SIZE + 1), (-340, SAMPLE_SIZE)]:
        sample = from_range(mi, ma)(SAMPLE_SIZE)
        assert_nonempty(sample)
        assert_elements_type(sample, int)


def test_range_float():
    for mi, ma in [(1, 20.0), (0.3, SAMPLE_SIZE + 1), (-1000.13, SAMPLE_SIZE + 0.1)]:
        sample = from_range(mi, ma)(SAMPLE_SIZE)
        assert_nonempty(sample)
        assert_elements_type(sample, float)


def test_const_int():
    sample = from_const(901)(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, int)
    assert_unique_count(sample, 1)
    assert_series_superset(sample, [901])


def test_const_float():
    sample = from_const(10.3)(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_elements_type(sample, float)
    assert_unique_count(sample, 1)
    assert_series_superset(sample, [10.3])


def test_add_generator():
    const1 = 33
    const2 = 2132
    gen1 = from_const(const1)
    gen2 = from_const(const2)
    sample = add(gen1, gen2)(100)
    assert_nonempty(sample)
    assert_elements_type(sample, int)
    assert_series_superset(sample, [const1 + const2])


def test_add_value():
    const = 33
    tests = [(10, int), (-3.2, float)]
    for val, t in tests:
        gen1 = from_const(const)
        sample = add(gen1, val)(100)
        assert_nonempty(sample)
        assert_elements_type(sample, t)
        assert_series_superset(sample, [const + val])


def test_subtract_generator():
    const1, const2 = 33, 2132
    gen1 = from_const(const1)
    gen2 = from_const(const2)
    sample = subtract(gen1, gen2)(100)
    assert_nonempty(sample)
    assert_elements_type(sample, int)
    assert_series_superset(sample, [const1 - const2])


def test_subtract_value():
    const = 33
    tests = [(10, int), (-3.2, float)]
    for val, t in tests:
        gen1 = from_const(const)
        sample = subtract(gen1, val)(100)
        assert_nonempty(sample)
        assert_elements_type(sample, t)
        assert_series_superset(sample, [const - val])


def test_subtract_from_generator():
    const1, const2 = 1032, 3123
    gen1, gen2 = from_const(const1), from_const(const2)
    sample = subtract_from(gen1, gen2)(809)
    assert_nonempty(sample)
    assert_series_superset(sample, [const2 - const1])


def test_subtract_from_value():
    const = 1032
    tests = [(10, int), (-3.2, float)]
    for val, t in tests:
        gen = from_const(val)
        sample = subtract_from(gen, const)(3232)
        assert_nonempty(sample)
        assert_series_superset(sample, [const - val])
        assert_elements_type(sample, t)


multi_tests = [(-32, -90, int), (32, 98.12, float), (1.23, 23.1, float)]


def test_multiply_generator():
    for const1, const2, t in multi_tests:
        gen1, gen2 = from_const(const1), from_const(const2)
        sample = multiply(gen1, gen2)(123)
        assert_nonempty(sample)
        assert_series_superset(sample, [const1 * const2])
        assert_elements_type(sample, t)


def test_multiply_value():
    for const1, const2, t in multi_tests:
        gen = from_const(const1)
        sample = multiply(gen, const2)(90843)
        assert_nonempty(sample)
        assert_series_superset(sample, [const1 * const2])
        assert_elements_type(sample, t)


def test_floor():
    floor_ = 15
    gen = lambda size: Series(range(size))
    sample = floor(gen, floor_)(12323)
    assert_nonempty(sample)
    assert_elements_type(sample, int)
    assert_all(sample, lambda el: el >= floor_, lambda el: f'Found value less than {floor_}: {el}')


def test_ceiling():
    ceil_ = 15
    gen = lambda size: Series(range(size))
    sample = ceiling(gen, ceil_)(12323)
    assert_nonempty(sample)
    assert_elements_type(sample, int)
    assert_all(sample, lambda el: el <= ceil_, lambda el: f'Found value greater than {ceil_}: {el}')


def test_round():
    decs = [(2, 2.33, float), (0, 2, int)]
    gen = lambda size: Series([2.326313321412329898] * size)
    for dec, exp, t in decs:
        sample = round_(gen, dec)(789392)
        assert_nonempty(sample)
        assert_elements_type(sample, t)
        assert_all(sample, lambda el: el == exp, lambda el: f'Expected {exp} but got {el}')
