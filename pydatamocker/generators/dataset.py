from typing import Iterable, Optional
from pydatamocker.exceptions.generator import DATASET_AND_PATH, UNSUPPORTED_DATASETS
from pydatamocker.types import ColumnGenerator
from ..util.data import load_data
import os.path as osp


DATASETS = {
    'first_name', 'last_name'
}

def from_dataset(dataset: str) -> ColumnGenerator:
    if dataset not in DATASETS:
            raise UNSUPPORTED_DATASETS(dataset)
    path = osp.join(osp.dirname(__file__), osp.pardir, 'data', dataset + '.pkl')
    data = load_data(path)
    func = lambda size: data.sample(n=size, replace=True).reset_index(drop=True)
    return func

def from_datapath(path: str, fields: Optional[Iterable[str]] = None) -> ColumnGenerator:
    data = load_data(path)
    samplesource = data[fields] if fields else data
    return lambda size: samplesource.sample(n=size, replace=True).reset_index(drop=True)


def create(**props) -> ColumnGenerator:
    dataset: Optional[str] = props.get('dataset')
    path: Optional[str] = props.get('path')
    if dataset and path:
        raise DATASET_AND_PATH(dataset, path)
    if dataset:
        return from_dataset(dataset)
    elif path:
        fields = props.get('fields')
        return from_datapath(path, fields)
    else:
        raise ValueError('Missing size')
