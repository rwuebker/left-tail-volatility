"""Daily measures only. Forward forecasting targets belong to Part 2."""
from .data import validate_series


def daily_variance(returns):
    validate_series(returns)
    return returns.pow(2).rename('daily_variance')


def daily_downside_variance(returns):
    """Squared negative returns around zero; preserve missing observations."""
    validate_series(returns)
    return returns.clip(upper=0).pow(2).rename('daily_downside_variance')
