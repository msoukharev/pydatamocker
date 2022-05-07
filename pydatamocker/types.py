from typing import Callable, Any, Iterable, Literal, Tuple, TypedDict, Union, get_args
from pandas import DataFrame, Series


ValueType = Literal['dataset', 'integer', 'float', 'enum', 'datetime']


NumericType = Literal['integer', 'float']


Dataset = Literal['first_name', 'last_name']


IntegerDistribution = Literal['binomial', 'normal', 'range', 'uniform']


FloatDistribution = Literal['normal', 'range', 'uniform']


DATASETS = get_args(Dataset)


TYPES = get_args(ValueType)


NUMERIC_TYPES = get_args(NumericType)


INTEGER_DISTRIBUTIONS = get_args(IntegerDistribution)


FLOAT_DISTRIBUTIONS = get_args(FloatDistribution)


class DistributionValue(TypedDict):
    distr: dict

class FieldSpec(TypedDict):
    type: ValueType


class TransformableField(TypedDict, total=False):
    filters: Iterable[Any]


class DatasetFieldSpec(FieldSpec):
    value: Dataset


class IntegerFieldSpec(FieldSpec, TransformableField):
    value: DistributionValue


class FloatFieldSpec(FieldSpec, TransformableField):
    value: DistributionValue


NumericFieldSpec = Union[IntegerFieldSpec, FloatFieldSpec]


class EnumFieldSpec(FieldSpec, TransformableField):
    value: dict


class DatetimeFieldSpec(FieldSpec, TransformableField):
    value: dict


class FieldToken(TypedDict):
    name: str
    spec: FieldSpec


Builder = Callable[[int, Iterable[FieldToken]], DataFrame]


ColumnGenerator = Callable[[int], Series]


ColumnGeneratorFactory = Callable[[Any], ColumnGenerator]
