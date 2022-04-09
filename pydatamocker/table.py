import json
from .builder import build

def create(title: str, config: dict = None):
    t = Table(title, config)
    return t

def createByLoading(title: str, config_path: str):
    t = Table(title, config_path = config_path)
    return t

class Table:

    def __init__(self, title: str, config: dict = None, config_path: str = None) -> None:
        if config and config_path:
            raise ValueError('Both config and config_path were specified')
        self.title = title
        if config_path:
            self.config = json.load(config_path)
        else:
            self.config = config or {
                'fields': {}
            }

    def dump_config(self, path, pretty=True, indent=2):

        def write_json(obj: dict, path: str, pretty: str, indent: int):
            with open(path, 'wt', ) as f:
                json.dump(obj, f, indent=(indent if pretty else None))

        write_json(self.config, path, pretty, indent)

    def field(self, name: str, **props):
        self.config['fields'][name] = props
        return self

    def sample(self, size: int):
        self.dataframe = build(size, self.config['fields'])
        return self.dataframe

    def reorder(self, order):
        fields = self.config['fields']
        neworderfields = dict()
        for col in order:
            neworderfields[col] = fields['col']

    def __str__(self):
        return self.dataframe.__str__()

    def __repr__(self):
        return self.dataframe.__repr__()
