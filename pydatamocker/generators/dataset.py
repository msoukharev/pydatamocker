from ..util.data import load_data
import os.path as osp

DATASETS = {
    'first_name', 'last_name'
}

def generate(size: int, **props):

    def generate_from_dataset(size, dataset):
        if dataset not in DATASETS:
            raise ValueError('Unsupported dataset')
        path = osp.join(osp.dirname(__file__), osp.pardir, 'data', dataset + '.pkl')
        data = load_data(path)
        return data.sample(n=size, replace=True).reset_index(drop=True)

    def generate_from_data(size, path, fields = None):
        data = load_data(path)
        samplesource = data[fields] if fields else data
        return samplesource.sample(n=size, replace=True).reset_index(drop=True)

    dataset = props.get('dataset')
    path = props.get('path')
    if dataset and path:
        raise ValueError('Both dataset and path are specified')
    if dataset:
        return generate_from_dataset(size, dataset)
    elif path:
        fields = props.get('fields')
        return generate_from_data(size, path, fields)
