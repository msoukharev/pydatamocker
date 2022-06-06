from typing import Collection, List, Dict
from pandas import Series
from pydatamocker.core.field.factory import get_generator
from pydatamocker.core.graph import graph
from pydatamocker.types import FieldBuildRequest, FieldBuildResult, FieldName, Field


def _apply(payload: FieldBuildRequest, build_results: Dict[FieldName, Series]) -> FieldBuildResult:
    size, field = payload
    series = get_generator(field['value'], build_results)(size)
    series.name = field['name'][1]
    return (field['name'], series)


def build(requests: Collection[FieldBuildRequest]) -> Collection[FieldBuildResult]:
    fields: List[Field] = [field for _, field in requests]
    requests_map = { field['name'] : (size, field ) for (size, field) in requests}
    levels = graph(fields)
    build_map: Dict[FieldName, Series] = {}
    for level in levels:
        build_map = {**build_map, **dict((_apply(requests_map[name], build_map) for name in level)) }
    return [(name, series) for name, series in build_map.items()]
