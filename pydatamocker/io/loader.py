import os.path as osp
from pandas import read_pickle


DATASETS = { 'first_name', 'last_name' }


_sr_cache = dict()


def load_dataset(dataset: str):
    if _sr_cache.get(dataset) is None:
        dataset_path = osp.join(osp.dirname(__file__), osp.pardir, 'data', dataset + '.pkl')
        _sr_cache[dataset] = read_pickle(dataset_path)
    return _sr_cache.get(dataset)
