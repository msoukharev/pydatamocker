from pandas import Series, DataFrame
import numpy as np


def base_props(**props):
    values = props['values']
    base_props = {
        'weights': [1] * len(values)
    }
    props = { **base_props, **props }
    return props


def get_sample(size: int, **props):
    props = base_props(**props)
    return Series(props['values']).sample(n=size, replace=True, weights=props['weights']).reset_index(drop=True)


def get_dependent_sample(controller_sample: Series, dep_name: str = '_dependent', **props):
    ctrl_name = controller_sample.name or '_controller'
    df = DataFrame({ ctrl_name: controller_sample })
    values = props['values']
    values_encoded = { controller : np.arange(len(opts)) for controller, opts in values.items() }
    df[dep_name] = df[ctrl_name].map(lambda ctrl: np.random.choice(values_encoded[ctrl]))
    df[dep_name] = df.apply(lambda row: values[row[ctrl_name]][row[dep_name]], axis=1)
    return df[dep_name]
