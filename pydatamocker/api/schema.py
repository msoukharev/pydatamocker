import json
import os
from typing import Collection, Dict
import asyncio
import aiofiles
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
        table_map = {k: {} for k in self.tables.keys()}
        for table in self.tables.values():
            for field_name in table.fields.keys():
                table_map[table._name][field_name] = result_map[(table._name), (field_name)]
        for table_name, mapped_data in table_map.items():
            self.tables[table_name]._data = DataFrame(mapped_data)


def from_dict(spec: Dict[str, Dict]) -> Schema:
    if len(spec) == 0:
        raise ValueError('No specs present')
    sch = Schema()
    for name, field_spec in spec.items():
        table = Table(name, field_spec['size'])
        for field in field_spec['fields']:
            table.field(field['name'], field['value'])
        sch.add(table)
    return sch


async def read_table_json(path: str) -> Table:
    async with aiofiles.open(path, 'rt') as f:
        content = json.loads(''.join(await f.readlines()))
        bname = os.path.splitext(os.path.basename(path))[0]
        table = Table(bname, content['size'])
        for field in content['fields']:
            table.field(field['name'], field['value'])
        return table


async def from_json(paths: Collection[str]) -> Schema:
    sch = Schema()
    tables = await asyncio.gather(
        *(read_table_json(path) for path in paths)
    )
    for table in tables:
        sch.add(table)
    return sch
