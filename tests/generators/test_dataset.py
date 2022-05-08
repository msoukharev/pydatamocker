from typing import Literal, get_args
import pytest
from pydatamocker.generators.dataset import create
from pydatamocker.types import DATASETS
from ..asserts import assert_equals


SAMPLE_SIZE = 1_000_000


# def test_no_nans_dataset():
#     for dataset in DATASETS:
#         sample = create({distr'': dataset, 'type': 'dataset' })(SAMPLE_SIZE)
#         assert_equals(0, sample.isna().sum(), f"Sample has NaN values. Dataset: {dataset}")
