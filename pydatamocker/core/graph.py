from functools import reduce
from typing import Collection, Dict, List, Set
from pydatamocker.types import Field, FieldName


# TODO: Cycle detection
def graph(fields: Collection[Field]) -> Collection[Collection[FieldName]]:
    adj: Dict[FieldName, Set[FieldName]] = { field['name']: set() for field in fields }
    def populate(field: Field):
        baseref = field['value'].get('ref')
        if baseref:
            adj[baseref].add(field['name'])
        filters = field['value'].get('filters')
        for filter in filters or ():
            filt_field = \
                filter.get('add') \
                or filter.get('subtract') \
                or filter.get('subtract_from') \
                or filter.get('multiply') \
                or filter.get('multiply')
            if isinstance(filt_field, dict):
                filt_ref = filt_field.get('ref')
                if filt_ref:
                    adj[filt_ref].add(field['name'])  # type: ignore
    for field in fields:
        populate(field)
    dependencies: Set[FieldName] = reduce(lambda st1, st2: st1.union(st2), adj.values())
    level: Set[FieldName] = set(adj.keys()).difference(dependencies)
    if not level:
        raise ValueError('Found no entry point for the field dependency graph')
    order: Dict[FieldName, int] = {}
    depth = 0
    while level:
        frontier = set()
        for field in level:
            order[field] = depth
            for dep in adj[field]:
                frontier.add(dep)

        level = frontier
        depth += 1

    levels: List[List[FieldName]] = [list() for _ in range(depth)]
    for fieldname, dp in order.items():
        levels[dp].append(fieldname)
    return levels
