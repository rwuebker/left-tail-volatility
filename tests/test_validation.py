import pandas as pd
import pytest
from left_tail.validation import chronological_split


def test_chronological_split_boundary_and_no_overlap():
    s = pd.Series(range(10), index=pd.date_range('2020-01-01', periods=10))
    train, test = chronological_split(s, '2020-01-06')
    assert len(train) == 6 and len(test) == 4
    assert train.index.max() < test.index.min()
    pd.testing.assert_series_equal(pd.concat([train, test]), s)


def test_changing_holdout_cannot_change_training():
    s = pd.Series(range(10), index=pd.date_range('2020-01-01', periods=10))
    altered = s.copy(); altered.iloc[6:] = 1000
    pd.testing.assert_series_equal(chronological_split(s, '2020-01-06')[0], chronological_split(altered, '2020-01-06')[0])


@pytest.mark.parametrize('cutoff', ['2019-01-01', '2021-01-01'])
def test_empty_split_rejected(cutoff):
    s = pd.Series(range(10), index=pd.date_range('2020-01-01', periods=10))
    with pytest.raises(ValueError):
        chronological_split(s, cutoff)
