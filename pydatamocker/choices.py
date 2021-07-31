from pandas import Series

def get_sample(size: int, **props):
    return Series(props['values']).sample(n=size, replace=True, weights=props['weights']).reset_index(drop=True)
