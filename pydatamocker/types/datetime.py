from datetime import datetime
import pandas as pd
from numpy import arange
from ..util.functions import composer
import datetime


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


def base_props(mock_type: str, **props):
    now = datetime.datetime.today()
    start = (now - datetime.timedelta(days=365)).strftime(default_formatter[mock_type])
    end = (now + datetime.timedelta(days=365)).strftime(default_formatter[mock_type])
    base_props = {
        'distr': 'range',
        'start': start,
        'end': end
    }
    props = { **base_props, **props }
    return props


def get_sample(mock_type: str, size: int, **kw):
    props = base_props(mock_type, props=kw)
    props['type'] = mock_type
    distr = props['distr']
    return pd.Series( _distribution_samples[distr](**{ **props, 'size' : size }) )
