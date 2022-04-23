import numpy as np
from pandas import Series

def _range_step(min: int, max: int, size: int) :
    return (max - min) / size

def float_normal(**props):
     return np.random.normal(props['mean'], props['std'], props['size'])

def float_uniform(**props):
    return np.random.uniform(props['min'], props['max'], props['size'])

def float_range(**props):
    return np.arange(props['start'], props['end'],
        _range_step(props['start'], props['end'], props['size'])).astype(float)[:props['size']]

def integer_uniform(**props):
    return np.random.randint(props['min'], props['max'], props['size'])

def integer_binomial(**props):
    return np.random.binomial(props['n'], props['p'], props['size'])

def integer_range(**props):
    return np.arange(props['start'], props['end'],
        _range_step(props['start'], props['end'], props['size'])).astype(int)[:props['size']]

def integer_normal(**props):
    # binomial approximation to normal
    # mean = n p
    # std = n p (1 - p)
    p = 1 - (props['std'] / props['mean'])
    n = round(props['mean'] / p)
    return integer_binomial(**{ 'n': n, 'p': p, 'size': props['size'] })

TYPES = { 'float', 'integer' }

def generate(size: int, **props) -> Series:
    switch_ = {
        'float': {
            'normal': float_normal,
            'uniform': float_uniform,
            'range': float_range
        },
        'integer': {
            'normal': integer_normal,
            'uniform': integer_uniform,
            'range': integer_range,
            'binomial': integer_binomial
        }
    }
    datatype = props['datatype']
    distr = props['distr']
    nums = switch_[datatype][distr](**{ **props, 'size': size })
    if distr == 'uniform' and props.get('round'):
        nums = np.around(nums, props['round'])
    return Series(nums)
