from pandas import DataFrame, concat
import pydatamocker.generators as gen
from pandas import Series, DataFrame
from .mocker import get_config

# from .generators.dataset import *
# from .generators.dataset import get_dataset_sample, get_table_sample, DATASETS
# from .generators.numeric import generate as num_generate, TYPES as NUMTYPES
# from .generators.datetime import generate as time_generate, TYPES as CHRONTYPES
# from .generators.enum import generate as enum_generate, generate_dependent as enum_generate_dep

def build(size: int, table_spec: dict) -> DataFrame:
    def match_generate(size, **props):
        datatype = props.get('datatype')
        dataset = props.get('dataset')
        if datatype and dataset:
            raise ValueError('Both datatype and dataset were specified')
        specifier = datatype or dataset
        if specifier in gen.dataset.DATASETS:
            return gen.dataset.generate(size, **props)
        elif specifier in gen.numeric.TYPES:
            return gen.numeric.generate(size, **props)
        elif specifier in gen.datetime.TYPES:
            return gen.enum.generate(size, **props)
        elif specifier == 'enum':
            return gen.enum.generate(size, **props)
        else:
            raise ValueError('Unsupported dataset or datatype ' + specifier)
    samples = DataFrame()
    for field_name, spec in table_spec.items():
        sample : Series = match_generate(size, **spec)
        samples[field_name] = sample
    return samples
