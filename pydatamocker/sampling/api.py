import pandas as pd
from .generators import get_sample_generator


def create_sample(mock_type: str, size: int, **props) -> pd.Series:
    sample_generator = get_sample_generator(mock_type, **props)
    return sample_generator(size)
