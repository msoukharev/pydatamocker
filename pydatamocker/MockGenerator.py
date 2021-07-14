from pandas import DataFrame
from .Field import Field
from numpy import arange
from .io.writer import write_dataframe
from .util.arguments import dedup_list, list_diff


class MockGenerator:

    dataframe: DataFrame
    field = dict()

    def add_field(self, field: Field):
        self.fields[field.name] = field

    def add_fields(self, *field_objects):
        for field_obj in field_objects:
            self.add_field(field_obj)

    def sample(self, size: int):
        column_order = ( self._column_order + list_diff(self.fields.keys(), self._column_order) ) or self.fields.keys()
        field_iterator = ( (name, self.fields[name]) for name in column_order )
        self.dataframe = DataFrame( data={ name: field.sample(size)
                                            for (name, field) in field_iterator },
                                    index=arange(size) )

    def get_dataframe(self):
        return self.dataframe.copy()

    def dump(self, path):
        if not path:
            raise ValueError('Path must be specified')
        write_dataframe(path, self.dataframe)

    def set_order(self, order):
        self._column_order = dedup_list(order)

    def __str__(self) -> str:
        self.dataframe.__str__()

    def __repr__(self) -> str:
        self.dataframe.__str__()
