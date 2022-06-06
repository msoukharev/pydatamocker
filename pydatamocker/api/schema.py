from typing import Collection, Dict

from pandas import DataFrame
from pydatamocker.api.table import Table
from pydatamocker.core.build import build
from pydatamocker.types import FieldBuildRequest


class Schema():

    def __init__(self) -> None:
        self.tables: Dict[str, Table] = {}

    def newTable(self, name: str, size: int) -> Table:
        table = Table(name, size)
        self.tables[name] = table
        return table

    def add(self, table: Table) -> Table:
        self.tables[table._name] = table
        return table

    def delete(self, name: str):
        if name in self.tables:
            del self.tables[name]

    def sample(self):
        build_requests: Collection[FieldBuildRequest] = []
        for table_name, table in self.tables.items():
            for field_name, field_value in table.fields.items():
                build_requests.append((
                    table._size,
                    {
                        'name': (table_name, field_name),
                        'value': field_value
                    }
                ))
        result_map = dict(build(build_requests))
        table_map = { k: {} for k in self.tables.keys() }
        for table in self.tables.values():
            for field_name in table.fields.keys():
                table_map[table._name][field_name] = result_map[(table._name), (field_name)]
        for table_name, mapped_data in table_map.items():
            self.tables[table_name]._data = DataFrame(mapped_data)
