from pandas import DataFrame
from multiprocessing import Pool
from pydatamocker.exceptions.builder import DATASET_AND_DATATYPE
from .generators import dataset, datetime, enum, numeric
from pandas import Series, DataFrame

def _switch(props):
    size = props['size']
    del props['size']
    datatype = props.get('datatype')
    dataset_ = props.get('dataset')
    if datatype and dataset_:
        raise DATASET_AND_DATATYPE(dataset_, datatype)
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

def build(size: int, table_spec: dict) -> DataFrame:

    samples = DataFrame()
    with Pool(6) as p:
        res = p.map(_switch, [
            {**field, 'name': name, 'size': size} for name, field in table_spec.items()
        ])
    for field_name, sample in zip(table_spec.keys(), res):
        samples[field_name] = sample
    return samples
