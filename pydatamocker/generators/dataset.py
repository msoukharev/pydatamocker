from typing import Optional
from pytest import param
from pydatamocker.exceptions.generator import UNSUPPORTED_DATASETS
from pydatamocker.types import ColumnGenerator, FieldParams
from ..util.data import load_data
import os.path as osp


DATASETS = {
    'first_name', 'last_name'
}


def from_dataset(dataset: str, restrict: Optional[int] = None) -> ColumnGenerator:
    if dataset not in DATASETS:
            raise UNSUPPORTED_DATASETS(dataset)
    if restrict != None and restrict < 1:
        raise ValueError(f'Parameter restrict should be at least 1. Got {restrict}')
    path = osp.join(osp.dirname(__file__), osp.pardir, 'data', dataset + '.pkl')
    data = load_data(path)
    if restrict != None and restrict < len(data):
        data = data.sample(restrict, replace=True).reset_index(drop=True)
    return lambda size: data.sample(size, replace=True).reset_index(drop=True)


def create(params: FieldParams) -> ColumnGenerator:
    try:
        dataset_name: str = params['dataset']['name']
        return from_dataset(dataset_name, restrict=params['dataset'].get('restrict'))
    except KeyError as _:
        raise ValueError(f'Unrecognized key: dataset. Provided value: {params} of type {FieldParams}')
