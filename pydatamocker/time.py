import pandas as pd
from numpy import arange
from .util.functions import compose
import datetime


default_formatter = {
    'datetime': '%Y-%m-%dT%H:%M:%SZ',
    'date': '%Y-%m-%d'
}


_distribution_samples = {
    'range': compose(False,
        lambda **kw: pd.date_range(start=kw['start'], end=kw['end'], periods=kw['size']),
        lambda f: lambda **kw: f(**kw).to_series(index=arange(kw['size'])),
        lambda f: lambda **kw: (f(**kw).dt.strftime(default_formatter[kw['type']])),
    ),
}
_distribution_samples['uniform'] = (
    compose(False,
        lambda **kw: pd.date_range(_distribution_samples['range'])(**kw),
        lambda f: lambda **kw: f(**kw).sample(frac=1).reset_index(drop=True)
    )
)


def get_sample(mock_type: str, size: int, **kw):
    kw['type'] = mock_type
    distr = kw['distr']
    return _distribution_samples[distr](**{ **kw, 'size' : size } )
