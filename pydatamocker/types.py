from typing import Callable, Any, Collection, Iterable, Literal, TypedDict, Union, get_args
from pandas import DataFrame, Series


# Literals


ValueType = Literal['dataset', 'integer', 'float', 'enum', 'datetime']


NumericType = Literal['integer', 'float']


Dataset = Literal['first_name', 'last_name']


IntegerDistribution = Literal['binomial', 'normal', 'range', 'uniform']


FloatDistribution = Literal['normal', 'range', 'uniform']


# Literals args


DATASETS = get_args(Dataset)


TYPES = get_args(ValueType)


NUMERIC_TYPES = get_args(NumericType)


INTEGER_DISTRIBUTIONS = get_args(IntegerDistribution)


FLOAT_DISTRIBUTIONS = get_args(FloatDistribution)


# Classes


class ValueDistribution(TypedDict, total=False):
    name: str
    min: Any
    max: Any
    start: Any
    end: Any
    mean: Any
    std: Any
    n: Any
    p: Any
    values: Collection[Any]
    weights: Collection[Any]


class FieldValue(TypedDict, total=False):
    distr: ValueDistribution
    const: Union[str, int, float]
    dataset: Dataset
    filters: Iterable['UnaryFilter']
    format: str


class UnaryFilter(FieldValue, TypedDict):
    operator: str


class FieldParams(FieldValue, TypedDict):
    type: ValueType


class FieldToken(TypedDict):
    name: str
    params: FieldParams


# Functions


Builder = Callable[[int, Iterable[FieldToken]], DataFrame]


ColumnGenerator = Callable[[int], Series]


ColumnGeneratorFactory = Callable[[Any], ColumnGenerator]
