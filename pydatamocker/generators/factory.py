from typing import cast
import pydatamocker.generators.datetime as datetime
import pydatamocker.generators.numeric as numeric
import pydatamocker.generators.dataset as dataset
import pydatamocker.generators.enum as enum
from pydatamocker.types import NUMERIC_TYPES, ColumnGenerator, FieldParams


def create(params: FieldParams) -> ColumnGenerator:
    type_ = params['type']
    if type_ == 'dataset':
        return dataset.create(params)
    elif type_ in NUMERIC_TYPES:
        return numeric.create(params)
    elif type_ == 'datetime':
        return datetime.create(params)
    elif type_ == 'enum':
        return enum.create(params)
    else:
        raise ValueError('No data typespecifier is provider')
