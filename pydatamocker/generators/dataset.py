from pytest import param
from pydatamocker.exceptions.generator import UNSUPPORTED_DATASETS
from pydatamocker.types import ColumnGenerator, FieldParams
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


def create(params: FieldParams) -> ColumnGenerator:
    try:
        dataset: str = params['dataset']
        return from_dataset(dataset)
    except KeyError as _:
        raise ValueError(f'Unrecognized key: dataset. Provided value: {params} of type {FieldParams}')
