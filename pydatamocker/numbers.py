import numpy as np
from .util.math import range_step

_dtype_distribution = {
    'float': {
        'normal': lambda props: lambda size: \
            np.random.normal(*[props.get(prop) for prop in ['mean', 'std']] + [size]),
        'uniform': lambda props: lambda size: \
            np.random.uniform(*[props.get(prop) for prop in ['min', 'max']] + [size]),
        'range': lambda props: lambda size: \
            np.arange(props['start'], props['end'], range_step(props['start'], props['end'], size)).astype(float)[:size]

    },
    'integer': {
        'uniform': lambda props: lambda size: \
            np.random.random_integers(*[props.get(prop) for prop in ['min', 'max']] + [size]),
        'binomial': lambda props: lambda size: \
            np.random.binomial(*[props.get(prop) for prop in ['n', 'p']] + [size]),
        'range': lambda props: lambda size: \
            np.floor(
                    np.arange(props['start'], props['end'], range_step(props['start'], props['end'], size)),
                ).astype(int)[:size]
    }
}


TYPES = { 'float', 'integer' }


DISTRIBUTIONS = {
    'normal': { 'mean', 'std' },
    'uniform': { 'min', 'max' },
    'binomial' : { 'n', 'p' },
    'range': { 'start', 'end' }
}


def get_distribution_sampler(dtype: str, distr: str, **props):
    return _dtype_distribution[dtype][distr](props)
