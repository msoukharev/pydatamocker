import os.path as osp
from pandas import read_pickle, read_csv, DataFrame
from pathlib import Path
import json
from .mocker import get_config


class _Datacache:

    data = {}

    def __init__(self):
        return

    def write(self, key: str, data, **kwargs):
        self.data[key] = { 'data': data }
        self.data[key].update(kwargs)

    def read(self, key: str):
        if not self.data.get(key):
            return None
        return self.data[key]['data']

    def get_props(self, key: str, *props):
        return { key: self.data[key][kw] for kw in props }

    def sample(self, key: str, size: int, field_s = None):
        sample_key = f"sample-{size}"
        sample = self.data[key].get(sample_key)
        if sample is None:
            sample = self.data[key]['data'].sample(size, replace=True).reset_index(drop=True)
            self.data[key][sample_key] = sample
        return sample if field_s is None else sample[field_s]


_cache = _Datacache()


_df_writers = {
    '.pkl' : lambda file, dataframe: dataframe.to_pickle(file, index=True),
    '.csv' : lambda file, dataframe: dataframe.to_csv(file, index=False),
    '.tsv' : lambda file, dataframe: dataframe.to_csv(file, sep="\t", index=False),
    '.json' : lambda file, dataframe: dataframe.to_json(file, orient='table', index=False)
}


get_dataset_path = lambda dataset: osp.join(osp.dirname(__file__), 'data', dataset + '.pkl')


DATASETS = { 'first_name', 'last_name' }


def _load_dataset(dataset: str):
    path = get_dataset_path(dataset)
    data = _cache.read(path)
    if data is None:
        data = read_pickle(path)
        _cache.write(path, data)


def _load_table(path: str):
    data = _cache.read(path)
    if data is None:
        data = read_csv(path)
        _cache.write(path, data)


def get_dataset_sample(name: str, size: int):
    _load_dataset(name)
    path = get_dataset_path(name)
    return _cache.sample(path, size)


def get_table_columns(path: str):
    _load_table(path)
    return _cache.read(path).columns


def get_table_sample(path: str, field_s: str, size: int):
    _load_table(path)
    return _cache.sample(path, size, field_s)


def write_dataframe(file: str, dataframe: DataFrame):
    report_progres = get_config('report_progress')
    report_progres and print(f"Dumping into file...")
    file_ext = Path(file).suffix
    if file_ext is None or not file_ext in _df_writers.keys():
        file_ext = '.csv'
    _df_writers[file_ext](file, dataframe)
    report_progres and print("Done!")


def load_json(file) -> dict:
    f = open(file, 'rt') if type(file) is str else file
    return json.load(f)


def write_json(obj: dict, path: str, pretty: str, indent: int):
    with open(path, 'wt', ) as f:
        json.dump(obj, f, indent=(indent if pretty else None))
