import numpy as np
from ..util.math import range_step
from ..util.functions import composer
from pandas import Series


_distribution_samples = {
    'float': {
        'normal': lambda **kw: composer(
            lambda **kw: np.random.normal(kw['mean'], kw['std'], kw['size']),
            **kw
        ),
        'uniform': lambda **kw: composer(
            lambda **kw: np.random.uniform(kw['min'], kw['max'], kw['size']),
            **kw
        ),
        'range': lambda **kw: composer(
            lambda **kw: np.arange(kw['start'], kw['end'], range_step(kw['start'], kw['end'], kw['size'])),
            lambda f, **kw: f.astype(float)[:kw['size']],
            **kw
        )
    },
    'integer': {
        'uniform': lambda **kw: composer(
            lambda **kw: np.random.randint(kw['min'], kw['max'], kw['size']),
            **kw
        ),
        'binomial': lambda **kw: composer(
            lambda **kw: np.random.binomial(kw['n'], kw['p'], kw['size']),
            **kw
        ),
        'range': lambda **kw: composer(
            lambda **kw: np.arange(kw['start'], kw['end'], range_step(kw['start'], kw['end'], kw['size'])),
            lambda f, **kw: f.astype(int)[:kw['size']],
            **kw
        )
    }
}


TYPES = { 'float', 'integer' }


DISTRIBUTIONS = {
    'normal': { 'mean', 'std' },
    'uniform': { 'min', 'max' },
    'binomial' : { 'n', 'p' },
    'range': { 'start', 'end' }
}


def base_props(dtype: str, size: int, **props):
    distr = props.get('distr') or 'uniform'
    if distr not in {'uniform', 'range'}:
        return props
    bound_labels = {
        'uniform': {
            'low': 'min',
            'high': 'max'
        },
        'range': {
            'low': 'start',
            'high': 'end'
        }
    }
    low = props.get('min') if dtype == 'normal' else props.get('start')
    high = props.get('max') if dtype == 'normal' else props.get('end')
    if not low and high:
        low = high - size
    elif not high and low:
        high = low + size
    else:
        low = low or 0
        high = high or size
    return {
        **props, **{
            'distr': distr,
            bound_labels[distr]['low']: low,
            bound_labels[distr]['high']: high
        }
    }


def get_sample(type_: str, size: int, **props):
    size = size or props['size']
    props = base_props(type_, size, **props)
    distr = props['distr']
    nums = _distribution_samples[type_][distr](**{**props, 'size': size})
    if distr == 'uniform' and props.get('round'):
        np.around(nums, props['round'])
    return Series(nums)
