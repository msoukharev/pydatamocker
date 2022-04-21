class DatasetGeneratorError(Exception):
    pass

def UNSUPPORTED_DATASETS(dataset):
    return DatasetGeneratorError('Unsupported dataset: ' + dataset)

def DATASET_AND_PATH(dataset, path):
    return DatasetGeneratorError(f'Both dataset [{dataset}] and path [{path}] specified')
