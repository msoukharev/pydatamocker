from ..util.data import load_data
import os.path as osp


DATASETS = {
    'first_name': {
        'description': 'Real first names of various origins'
    },
    'last_name': {
        'description': 'Read last names of various origins'
    }
}


DATASET_KEYS = DATASETS.keys()


def get_dataset_path(dataset: str):
    if dataset not in DATASET_KEYS:
        return None
    return osp.join(osp.dirname(__file__), osp.pardir, 'data', dataset + '.pkl')


def get_dataset_sample(dataset: str, size: int):
    path = get_dataset_path(dataset)
    data = load_data(path)
    return data.sample(n=size, replace=True).reset_index(drop=True)


def get_table_sample(path: str, field_s: str, size: int):
    data = load_data(path)
    return data[field_s].sample(n=size, replace=True).reset_index(drop=True)
