from typing import cast
import pydatamocker.generators.datetime as datetime
import pydatamocker.generators.numeric as numeric
import pydatamocker.generators.dataset as dataset
import pydatamocker.generators.enum as enum
from pydatamocker.types import NUMERIC_TYPES, ColumnGenerator, DatasetFieldSpec, DatetimeFieldSpec, EnumFieldSpec, FieldSpec, NumericFieldSpec


def create(spec: FieldSpec) -> ColumnGenerator:
    type_ = spec['type']
    if type_ == 'dataset':
        spec = cast(DatasetFieldSpec, spec)
        return dataset.create(spec)
    elif type_ in NUMERIC_TYPES:
        spec = cast(NumericFieldSpec, spec)
        return numeric.create(spec)
    elif type_ == 'datetime':
        spec = cast(DatetimeFieldSpec, spec)
        return datetime.create(spec)
    elif type_ == 'enum':
        spec = cast(EnumFieldSpec, spec)
        return enum.create(spec)
    else:
        raise ValueError('No data typespecifier is provider')
