from typing import Callable

from pandas import Series

import pydatamocker.generators.datetime as datetime
import pydatamocker.generators.numeric as numeric
import pydatamocker.generators.dataset as dataset
import pydatamocker.generators.enum as enum

def factory(**props) -> Callable[[], Series]:
    datatype = props.get('datatype')
    dataset_ = props.get('dataset')
    if datatype and dataset_:
        raise ValueError('Both dataset and datatype specified')
    specifier = datatype or dataset_
    if specifier in dataset.DATASETS:
        return dataset.generate
    elif specifier in numeric.TYPES:
        return numeric.generate
    elif specifier in datetime.TYPES:
        return datetime.generate
    elif specifier == 'enum':
        return enum.generate
    else:
        raise ValueError('No data typespecifier is provider')
