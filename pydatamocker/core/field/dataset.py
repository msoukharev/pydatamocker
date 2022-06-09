from typing import Optional
from pydatamocker.types import FieldGenerator, DATASETS
from pydatamocker.util.data import load_data
import os.path as osp


def from_dataset(dataset: str, restrict: Optional[int] = None) -> FieldGenerator:
    if dataset not in DATASETS:
        raise ValueError(f'Unsupported dataset {dataset}')
    if restrict is not None and restrict < 1:
        raise ValueError(f'Parameter restrict should be at least 1. Got {restrict}')
    path = osp.join(osp.dirname(__file__), osp.pardir, osp.pardir, 'data', dataset + '.pkl')
    data = load_data(path)
    if restrict is not None and restrict < len(data):
        data = data.sample(restrict, replace=True).reset_index(drop=True)
    return lambda size: data.sample(size, replace=True).reset_index(drop=True)
