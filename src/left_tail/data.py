"""Daily data checks and simple adjusted-close returns."""
import numpy as np
import pandas as pd


def validate_series(series: pd.Series) -> None:
    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError('A DatetimeIndex is required')
    if series.empty or series.index.hasnans or not series.index.is_unique or not series.index.is_monotonic_increasing:
        raise ValueError('Dates must be nonempty, unique, valid, and increasing')
    if np.isinf(series.to_numpy(dtype=float)).any():
        raise ValueError('Infinite values are invalid')


def daily_returns(prices: pd.Series) -> pd.Series:
    """Decimal simple returns; missing prices are never forward-filled."""
    validate_series(prices)
    if (prices.dropna() <= 0).any():
        raise ValueError('Prices must be positive')
    return prices.pct_change(fill_method=None).rename('return')


def audit_series(series: pd.Series, reference_dates: pd.DatetimeIndex) -> dict:
    """Missing counts relative to observed SPY dates, not an exchange calendar."""
    validate_series(series)
    valid = series.dropna()
    return {
        'rows': len(series), 'usable': len(valid), 'missing_in_source_rows': int(series.isna().sum()),
        'first_usable': str(valid.index.min().date()) if len(valid) else None,
        'last_usable': str(valid.index.max().date()) if len(valid) else None,
        'missing_on_SPY_dates': int(series.reindex(reference_dates).isna().sum()),
    }
