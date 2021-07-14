import pandas as pd
from .sampling import create_sample

class Field:

    name: str
    mock_type: str
    props: dict

    series: pd.Series

    def __init__(self, name: str, mock_type: str, **props):
        self.name = name
        self.mock_type = mock_type
        self.props = props if props else dict()

    def set_props(self, **props):
        self.props.update(props)

    def set_prop(self, name, val):
        self.set_props(**{ name: val })

    def sample(self, size) -> pd.Series:
        return pd.Series(create_sample(self.mock_type, size, **self.props))

    def get_series(self) -> pd.Series:
        return self.series.copy()

    def __str__(self) -> str:
        self.series.__str__()

    def __repr__(self) -> str:
        self.series.__repr__()
