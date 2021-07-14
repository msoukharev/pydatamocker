import pandas as pd
from pathlib import Path


DATAFRAME_WRITER = {
    'pkl' : lambda file, dataframe: dataframe.to_pickle(file, index=True),
    'csv' : lambda file, dataframe: dataframe.to_csv(file, index=False),
    'tsv' : lambda file, dataframe: dataframe.to_csv(file, sep='\t', index=False),
    'json' : lambda file, dataframe: dataframe.to_json(file, index=False)
}


def write_dataframe(file: str, dataframe: pd.DataFrame):
    file_ext = Path(file).suffix
    if file_ext is None or not file_ext in DATAFRAME_WRITER.keys():
        file_ext = 'csv'
    DATAFRAME_WRITER[file_ext](file, dataframe)
