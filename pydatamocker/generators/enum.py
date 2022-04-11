from pandas import Series
from math import ceil
from numpy import chararray, array, concatenate, repeat

DISTRIBUTIONS = { 'ordered', 'shuffled' }

def generate(size: int, **props):
    values = props['values']
    weights = props.get('weights') or [1] * len(values)
    distr = props.get('distr') or 'ordered'
    if distr == 'ordered':
        weightsum = sum(weights)
        counts = [ ceil(size * (w / weightsum)) for w in weights ]
        sections = tuple(repeat(val, count) for (val, count) in zip(values, counts))
        arrays = concatenate(sections, axis=None)
        return Series(data=arrays[:size])
    elif distr == 'shuffled':
        return Series(values).sample(n=size, replace=True, weights=weights).reset_index(drop=True)

# def generate_dependent(controller_sample: Series, dep_name: str, **props):
#     ctrl_name = controller_sample.name or '_controller'
#     df = DataFrame({ ctrl_name: controller_sample })
#     values = props['values']
#     values_encoded = { controller : np.arange(len(opts)) for controller, opts in values.items() }
#     df[dep_name] = df[ctrl_name].map(lambda ctrl: np.random.choice(values_encoded[ctrl]))
#     df[dep_name] = df.apply(lambda row: values[row[ctrl_name]][row[dep_name]], axis=1)
#     return df[dep_name]
