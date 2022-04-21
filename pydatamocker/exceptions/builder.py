class BuilderException(Exception):
    pass

def DATASET_AND_DATATYPE(dataset, datatype):
    return BuilderException(f'Both dataset [{dataset}] and datatype [{datatype}]')
