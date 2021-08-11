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


def get_sample(dtype: str, size: int = None, **props):
    size = size or props['size']
    distr = props['distr']
    return Series( _distribution_samples[dtype][distr](**{**props, 'size': size}) )