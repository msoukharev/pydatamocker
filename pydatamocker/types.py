from typing import *
from pandas import DataFrame, Series


ColumnGenerator = Callable[[int], Series]


ColumnGeneratorFactory = Callable[[Any], ColumnGenerator]


Builder = Callable[[Any], DataFrame]
