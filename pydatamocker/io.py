import os.path as osp
from pandas import read_pickle, DataFrame
from pathlib import Path
import json


class _Datacache:

    data = dict()

    def __init__(self):
        return

    def write(self, key: str, dataset, path: str = None):
        self.data[key] = { 'dataset': dataset }
        if path:
            self.data[key]['path'] = path
        return self.data[key]

    def read(self, key: str):
        if not self.data.get(key):
            return None
        return self.data[key]['dataset']


_cache = _Datacache()


_df_writers = {
    '.pkl' : lambda file, dataframe: dataframe.to_pickle(file, index=True),
    '.csv' : lambda file, dataframe: dataframe.to_csv(file, index=False),
    '.tsv' : lambda file, dataframe: dataframe.to_csv(file, sep="\t", index=False),
    '.json' : lambda file, dataframe: dataframe.to_json(file, orient='table', index=False)
}


DATASETS = { 'first_name', 'last_name' }


def load_dataset(dataset: str):
    data = _cache.read(dataset)
    if data is None:
        path = osp.join(osp.dirname(__file__), osp.pardir, 'data', dataset + '.pkl')
        data = read_pickle(path)
        _cache.write(dataset, data, path)
    return data


def write_dataframe(file: str, dataframe: DataFrame):
    file_ext = Path(file).suffix
    if file_ext is None or not file_ext in _df_writers.keys():
        file_ext = '.csv'
    _df_writers[file_ext](file, dataframe)


def load_json(file) -> dict:
    f = open(file, 'rt') if type(file) is str else file
    return json.load(f)


def write_json(obj: dict, path: str, pretty: str, indent: int):
    with open(path, 'wt', ) as f:
        json.dump(obj, f, indent=(indent if pretty else None))
