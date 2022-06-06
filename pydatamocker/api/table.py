from typing import Dict, Optional

from pandas import DataFrame

from pydatamocker.types import Value


class Table():

    def __init__(self, name: str, size: int) -> None:
        self.fields: Dict[str, Value] = {}
        self._name = name
        if size < 1:
            raise ValueError('Size cannot be less that 1')
        self._size = size
        self._data: DataFrame = DataFrame()

    def field(self, name: str, value: Value):
        self.fields[name] = value

    def getData(self) -> DataFrame:
        return self._data
