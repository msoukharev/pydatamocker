import numpy as np
from ..util.functions import composer
from pandas import Series

def _range_step(min_: int, max_: int, size: int) :
    return (max_ - min_) / size

samplers : dict = {
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
            lambda **kw: np.arange(kw['start'], kw['end'], _range_step(kw['start'], kw['end'], kw['size'])),
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
            lambda **kw: np.arange(kw['start'], kw['end'], _range_step(kw['start'], kw['end'], kw['size'])),
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

def generate(size: int, **props) -> Series:
    datatype = props['datatype']
    distr = props['distr']
    nums = samplers[datatype][distr](**{ **props, 'size': size })
    if distr == 'uniform' and props.get('round'):
        nums = np.around(nums, props['round'])
    return Series(nums)
