from pandas import Series
from pydatamocker.exceptions.generator import DATASET_AND_PATH, UNSUPPORTED_DATASETS
from ..util.data import load_data
import os.path as osp

DATASETS = {
    'first_name', 'last_name'
}

def generate(**props) -> Series:

    def generate_from_dataset(size, dataset):
        if dataset not in DATASETS:
            raise UNSUPPORTED_DATASETS(dataset)
        path = osp.join(osp.dirname(__file__), osp.pardir, 'data', dataset + '.pkl')
        data = load_data(path)
        return data.sample(n=size, replace=True).reset_index(drop=True)

    def generate_from_data(size, path, fields = None):
        data = load_data(path)
        samplesource = data[fields] if fields else data
        return samplesource.sample(n=size, replace=True).reset_index(drop=True)

    dataset = props.get('dataset')
    path = props.get('path')
    size = props['size']
    if dataset and path:
        raise DATASET_AND_PATH(dataset, path)
    if dataset:
        return generate_from_dataset(size, dataset)
    elif path:
        fields = props.get('fields')
        return generate_from_data(size, path, fields)
    else:
        raise ValueError('Missing size')
