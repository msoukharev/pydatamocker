from pandas import DataFrame, concat

from .mocker import get_config
# from .generators.dataset import *
# from .generators.dataset import get_dataset_sample, get_table_sample, DATASETS
# from .generators.numeric import generate as num_generate, TYPES as NUMTYPES
# from .generators.datetime import generate as time_generate, TYPES as CHRONTYPES
# from .generators.enum import generate as enum_generate, generate_dependent as enum_generate_dep

import pydatamocker.generators as gen
from pandas import Series, DataFrame

def match_generate(size, **props):
    datatype = props['datatype']
    if datatype in gen.dataset.DATASETS:
        return gen.dataset.generate(size, **props)
    elif datatype in gen.numeric.TYPES:
        return gen.numeric.generate(size, **props)
    elif datatype == 'enum':
        return gen.enum.generate(size, **props)
    elif datatype in gen.datetime.TYPES:
        return gen.enum.generate(size, **props)
    else:
        raise ValueError('Unsupported type ' + datatype)

def build_dataframe(size: int, table_spec: dict) -> DataFrame:
    samples = []
    for field_name, spec in table_spec['fields'].items():
        sample : Series = match_generate(size, **spec)
        sample.name = field_name
        samples.append(sample)
    return DataFrame(samples)
