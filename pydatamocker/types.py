from typing import Callable, Any, Collection, Iterable, Literal, TypeVar, TypedDict, Union, get_args
from pandas import DataFrame, Series


N = TypeVar('N', int, float)


# Literals


ValueType = Literal['dataset', 'number', 'enum', 'datetime']


Dataset = Literal['first_name', 'last_name']


NumericDistribution = Literal['binomial', 'normal', 'range', 'uniform']


FilterOperator = Literal['add', 'subtract', 'subtract_from', 'floor', 'ceiling', 'round']


# Literals args


DATASETS = get_args(Dataset)


TYPES = get_args(ValueType)


NUMERIC_DISTRIBUTIONS = get_args(NumericDistribution)


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


class DatasetValueParams(TypedDict, total=False):
    restrict: int


class DatasetValue(DatasetValueParams, TypedDict):
    name: Dataset


class FieldValue(TypedDict, total=False):
    distr: ValueDistribution
    const: Union[int, float]
    dataset: DatasetValue
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
