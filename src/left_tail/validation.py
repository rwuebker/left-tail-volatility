"""Chronological holdout for contemporaneous daily returns in Part 1."""
import pandas as pd
from .data import validate_series


def chronological_split(series, train_end):
    """No forward labels here. Part 2 must purge overlapping target windows."""
    validate_series(series)
    cutoff = pd.Timestamp(train_end)
    train, test = series.loc[series.index <= cutoff], series.loc[series.index > cutoff]
    if train.empty or test.empty or series.isna().any():
        raise ValueError('Require nonempty train/test sets and complete values')
    return train.copy(), test.copy()
