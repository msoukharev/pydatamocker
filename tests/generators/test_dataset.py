import pytest
from pydatamocker.generators.dataset import generate, DATASETS
from ..asserts import assert_equals

SAMPLE_SIZE = 1_000_000

def test_no_nans_dataset():
    for dataset in DATASETS:
        sample = generate(SAMPLE_SIZE, **{ 'dataset': dataset })
        assert_equals(0, sample.isna().sum(), f"Sample has NaN values. Dataset: {dataset}")
