import pandas as pd
from numpy import arange
from ..util.functions import composer


default_formatter = {
    'datetime': '%Y-%m-%dT%H:%M:%SZ',
    'date': '%Y-%m-%d'
}


_distribution_samples = {
    'range': lambda **kw: composer(
        lambda **kw: pd.date_range(start=kw['start'], end=kw['end'], periods=kw['size']),
        lambda f, **kw: f.to_series(index=arange(kw['size'])),
        lambda f, **kw: f.dt.strftime(default_formatter[kw['type']]),
        **kw
    ),
}
_distribution_samples['uniform'] = (
    lambda **kw: composer(
        lambda **kw: _distribution_samples['range'](**kw),
        lambda f, **kw: f.sample(frac=1).reset_index(drop=True),
        **kw
    )
)


def get_sample(mock_type: str, size: int, **kw):
    kw['type'] = mock_type
    distr = kw['distr']
    return pd.Series( _distribution_samples[distr](**{ **kw, 'size' : size }) )
