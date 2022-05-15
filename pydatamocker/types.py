from typing import Callable, Any, Collection, Iterable, Literal, TypeVar, TypedDict, Union, get_args
from pandas import DataFrame, Series


N = TypeVar('N', int, float)


# Literals


ValueType = Literal['dataset', 'integer', 'float', 'enum', 'datetime']


NumericType = Literal['integer', 'float']


Dataset = Literal['first_name', 'last_name']


IntegerDistribution = Literal['binomial', 'normal', 'range', 'uniform']


FloatDistribution = Literal['normal', 'range', 'uniform']


FilterOperator = Literal['add', 'subtract', 'subtract_from', 'floor', 'ceiling']


# Literals args


DATASETS = get_args(Dataset)


TYPES = get_args(ValueType)


NUMERIC_TYPES = get_args(NumericType)


INTEGER_DISTRIBUTIONS = get_args(IntegerDistribution)


FLOAT_DISTRIBUTIONS = get_args(FloatDistribution)


FILTER_OPERATORS = get_args(FilterOperator)


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
    const: Union[int, float]
    dataset: Dataset
    filters: Iterable['UnaryFilter']
    format: str
    literal: str


class FieldParams(FieldValue, TypedDict):
    type: ValueType


class FieldToken(TypedDict):
    name: str
    params: FieldParams


class UnaryFilter(TypedDict):
    operator: FilterOperator
    argument: FieldParams


# Functions


Builder = Callable[[int, Iterable[FieldToken]], DataFrame]


ColumnGenerator = Callable[[int], Series]


FilteredColumnGenerator = Callable[[UnaryFilter, ColumnGenerator], ColumnGenerator]


ColumnGeneratorFactory = Callable[[Any], ColumnGenerator]
