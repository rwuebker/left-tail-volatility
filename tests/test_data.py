import numpy as np
import pandas as pd
import pytest
from left_tail.data import daily_returns, audit_series


def series(values):
    return pd.Series(values, index=pd.date_range('2020-01-01', periods=len(values)))


def test_returns_known_prices():
    np.testing.assert_allclose(daily_returns(series([100., 110., 99.])).iloc[1:], [.1, -.1])


def test_missing_prices_never_filled():
    actual = daily_returns(series([100., np.nan, 110., 121.]))
    assert actual.iloc[:3].isna().all()
    assert actual.iloc[3] == pytest.approx(.1)


@pytest.mark.parametrize('values', [[100, 0], [100, -1], [100, np.inf]])
def test_invalid_prices(values):
    with pytest.raises(ValueError):
        daily_returns(series(values))


def test_reject_unsorted_and_duplicate_dates():
    for index in [pd.to_datetime(['2020-01-02', '2020-01-01']), pd.to_datetime(['2020-01-01'] * 2)]:
        with pytest.raises(ValueError):
            daily_returns(pd.Series([1., 2.], index=index))


def test_audit_distinguishes_rows_and_reference_gaps():
    s = series([10., np.nan, 12.])
    result = audit_series(s, pd.date_range('2020-01-01', periods=4))
    assert result['usable'] == 2
    assert result['missing_in_source_rows'] == 1
    assert result['missing_on_SPY_dates'] == 2


def test_future_price_change_does_not_change_past_returns():
    a = series([100., 101., 102., 103.]); b = a.copy(); b.iloc[-1] = 999.
    pd.testing.assert_series_equal(daily_returns(a).iloc[:-1], daily_returns(b).iloc[:-1])
