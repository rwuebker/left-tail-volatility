import numpy as np
import pandas as pd
from left_tail.targets import daily_variance, daily_downside_variance


def test_daily_measures_known_example_and_missing():
    r = pd.Series([.04, -.04, 0., -.02, np.nan], index=pd.date_range('2020-01-01', periods=5))
    np.testing.assert_allclose(daily_variance(r), [.0016, .0016, 0., .0004, np.nan], equal_nan=True)
    np.testing.assert_allclose(daily_downside_variance(r), [0., .0016, 0., .0004, np.nan], equal_nan=True)


def test_downside_never_exceeds_total():
    r = pd.Series(np.random.default_rng(42).normal(size=100), index=pd.date_range('2020-01-01', periods=100))
    assert (daily_downside_variance(r) <= daily_variance(r)).all()


def test_squared_returns_mean_variance_identity():
    r = np.array([.01, .02, -.01, .03])
    np.testing.assert_allclose(np.mean(r**2), np.var(r, ddof=0) + r.mean()**2)
