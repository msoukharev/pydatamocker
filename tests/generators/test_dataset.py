import pytest
from pydatamocker.generators.dataset import create
from pydatamocker.types import DATASETS
from tests.util import assert_nonempty, assert_unique_count
from ..asserts import assert_equals


SAMPLE_SIZE = 1_000_000


def test_no_nans_dataset():
    for dataset in DATASETS:
        sample = create({'dataset': { 'name': dataset }, 'type': 'dataset' })(SAMPLE_SIZE)
        assert_nonempty(sample)


def test_restrict():
    restr = 3
    sample = create({'dataset': { 'name': 'first_name', 'restrict': restr }, 'type': 'dataset'})(SAMPLE_SIZE)
    assert_nonempty(sample)
    assert_unique_count(sample, 3)
