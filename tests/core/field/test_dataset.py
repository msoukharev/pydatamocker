import pytest
from pydatamocker.core.field.dataset import from_dataset
from pydatamocker.types import DATASETS
from tests.util import assert_nonempty, assert_unique_count


SAMPLE_SIZE = 1_000_000


def test_dataset():
    for dataset in DATASETS:
        sample = from_dataset(dataset)(SAMPLE_SIZE)
        assert_nonempty(sample)


def test_restrict():
    restr = 11
    sample = from_dataset(DATASETS[0], restrict=restr)(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_unique_count(sample, restr)
