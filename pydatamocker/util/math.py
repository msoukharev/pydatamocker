from math import ceil


def range_step(min_: int, max_: int, size: int):
    if max_ > size:
        return ceil( (max_ - min_) / size)
    else:
        return (max_ - min_) / size
