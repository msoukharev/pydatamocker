import numpy.random as npr


_dtype_distribution = {
    'float': {
        'normal': lambda props: lambda size: npr.normal(*[props.get(prop) for prop in ['mean', 'std']] + [size]),
        'uniform': lambda props: lambda size: npr.uniform(*[props.get(prop) for prop in ['min', 'max']] + [size])
    },
    'integer': {
        'uniform': lambda props: lambda size: npr.random_integers(*[props.get(prop) for prop in ['min', 'max']] + [size]),
        'binomial': lambda props: lambda size: npr.binomial(*[props.get(prop) for prop in ['n', 'p']] + [size])
    }
}


RANDOM_TYPES = { 'float', 'integer' }


RANDOM_SET_PARAMS = {
    'normal': { 'mean', 'std' },
    'uniform': { 'min', 'max' },
    'binomial' : { 'n', 'p' }
}


def get_distribution_sampler(dtype: str, distr: str, **props):
    return _dtype_distribution[dtype][distr](props)
