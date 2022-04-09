from pandas import DataFrame
from .generators import dataset, datetime, enum, numeric
from pandas import Series, DataFrame

def build(size: int, table_spec: dict) -> DataFrame:
    def match_generate(size, **props):
        datatype = props.get('datatype')
        dataset_ = props.get('dataset')
        if datatype and dataset_:
            raise ValueError('Both datatype and dataset were specified')
        specifier = datatype or dataset_
        if specifier in dataset.DATASETS:
            return dataset.generate(size, **props)
        elif specifier in numeric.TYPES:
            return numeric.generate(size, **props)
        elif specifier in datetime.TYPES:
            return datetime.generate(size, **props)
        elif specifier == 'enum':
            return enum.generate(size, **props)
        else:
            raise ValueError('Unsupported dataset or datatype ' + specifier)
    samples = DataFrame()
    for field_name, spec in table_spec.items():
        sample : Series = match_generate(size, **spec)
        samples[field_name] = sample
    return samples
