import pydatamocker.generators.datetime as datetime
import pydatamocker.generators.numeric as numeric
import pydatamocker.generators.dataset as dataset
import pydatamocker.generators.enum as enum
from pydatamocker.types import ColumnGenerator


def create(**props) -> ColumnGenerator:
    datatype = props.get('datatype')
    dataset_ = props.get('dataset')
    if datatype and dataset_:
        raise ValueError('Both dataset and datatype specified')
    specifier = datatype or dataset_
    if specifier in dataset.DATASETS:
        return dataset.create(**props)
    elif specifier in numeric.TYPES:
        return numeric.create(**props)
    elif specifier in datetime.TYPES:
        return datetime.create(**props)
    elif specifier == 'enum':
        return enum.create(**props)
    else:
        raise ValueError('No data typespecifier is provider')
