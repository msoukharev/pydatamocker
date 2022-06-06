from dataclasses import Field
from typing import Any, Callable, Collection, List, Literal, Tuple, TypedDict, Union, get_args
from pandas import DataFrame, Series


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

class Normal(TypedDict):
    mean: Union[int, float]
    std: Union[int, float]


class Binomial(TypedDict):
    n: int
    p: float


class Range(TypedDict, total=False):
    start: Union[int, float, str]
    end: Union[int, float, str]
    format: str


class Uniform(TypedDict, total=False):
    min: Union[int, float, str]
    max: Union[int, float, str]
    format: str


FieldName = Tuple[str, str]


class DatasetValue(TypedDict, total=False):
    name: str
    restrict: int


class EnumValue(TypedDict, total=False):
    values: List[Any]
    counts: List[Union[int, float]]
    shuffle: bool

class Value(TypedDict, total=False):
    const: Union[int, float, str]
    dataset: DatasetValue
    normal: Normal
    binomial: Binomial
    range: Range
    uniform: Uniform
    filters: Collection['FieldModificator']
    enum: EnumValue
    ref: FieldName


class FieldModificator(TypedDict, total=False):
    add: Union[Value, int, float]
    subtract: Union[Value, int, float]
    subtract_from: Union[Value, int, float]
    multiply: Union[Value, int, float]
    floor: Union[int, float]
    ceiling: Union[int, float]
    round: int


class Field(TypedDict):
    name: FieldName
    value: Value


FieldBuildRequest = Tuple[int, Field]


FieldBuildResult = Tuple[FieldName, Series]


# Functions


Builder = Callable[[Collection[FieldBuildRequest]], Collection[Series]]


FieldGenerator = Callable[[int], Series]


ModifiedFieldGenerator = Callable[[FieldModificator, FieldGenerator], FieldGenerator]
