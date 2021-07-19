from pandas import DataFrame
from .Field import Field
from numpy import arange
from .io.writer import write_dataframe
from .util.arguments import dedup_list, list_diff


class MockGenerator:

    dataframe: DataFrame
    fields_describe = dict()

    def add_field(self, name: str, mock_type:str, **props):
        self.fields_describe[name] = {
            'mock_type': mock_type,
            'props': props
        }

    def add_fields(self, fields_describe: dict):
        self.fields_describe.update(fields_describe)

    def sample(self, size: int):
        column_order = ( self._column_order + list_diff(self.fields_describe.keys(), self._column_order) ) or self.fields_describe.keys()
        field_iterator = ( (name,
            Field(name, self.fields_describe[name]['mock_type'], **self.fields_describe[name]['props'])) for name in column_order )
        self.dataframe = DataFrame( data={ name: field.sample(size)
                                            for (name, field) in field_iterator },
                                    index=arange(size) )

    def get_dataframe(self):
        return self.dataframe.copy()

    def dump(self, path):
        if not path:
            raise ValueError('Path must be specified')
        write_dataframe(path, self.dataframe)

    def set_column_order(self, order):
        self._column_order = dedup_list(order)

    def __str__(self) -> str:
        self.dataframe.__str__()

    def __repr__(self) -> str:
        self.dataframe.__str__()
