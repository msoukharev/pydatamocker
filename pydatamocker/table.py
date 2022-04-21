import json
from pydatamocker.exceptions.table import NO_SIZE, NO_TITLE
from .builder import build

def createEmpty(title: str):
    t = Table({ 'title': title})
    return t

def createFromConfig(config: dict):
    return Table(config)

def createFromJSON(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        return createFromConfig(config)

class Table:

    def __init__(self, config: dict) -> None:
        if not config.get('title'):
            raise NO_TITLE()
        config_ = dict(config)
        config_['fields'] = config.get('fields') or {}
        self.config = config_

    def dump_config(self, path, pretty=True, indent=2):

        def write_json(obj: dict, path: str, pretty: str, indent: int):
            with open(path, 'wt', ) as f:
                json.dump(obj, f, indent=(indent if pretty else None))

        write_json(self.config, path, pretty, indent)

    def field(self, name: str, **props):
        self.config['fields'][name] = props
        return self

    def sample(self, size: int = None):
        if not size and not self.config.get('size'):
            raise NO_SIZE()
        size_ = size or self.config['size']
        self.dataframe = build(size_, self.config['fields'])
        return self.dataframe

    def reorderFields(self, order):
        fields = self.config['fields']
        neworderfields = { field:fields[field] for field in order }
        remainder = { field:fields[field] for field in fields.keys() if field not in set(order) }
        neworderfields = {
            **neworderfields,
            **remainder
        }
        self.config['fields'] = neworderfields

    def __str__(self):
        return self.dataframe.__str__()

    def __repr__(self):
        return self.dataframe.__repr__()
