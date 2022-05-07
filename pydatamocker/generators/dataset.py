from typing import Iterable, Optional
from pydatamocker.exceptions.generator import UNSUPPORTED_DATASETS
from pydatamocker.types import ColumnGenerator, DatasetFieldSpec, FieldSpec
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

def create(spec: DatasetFieldSpec) -> ColumnGenerator:
    dataset: str = spec['value']
    if dataset:
        return from_dataset(dataset)
    else:
        raise ValueError('Missing size')
