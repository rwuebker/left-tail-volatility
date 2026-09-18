"""Causal fixed-parameter forecasts and a self-financing SPY/cash experiment.

The five-day downside expectation uses Monte Carlo simulation of GJR-t paths,
including the estimated mean. Allocation thresholds are explicitly heuristic.
"""
import numpy as np
import pandas as pd
from .data import validate_series
from .garch import next_variance


def gjr_downside_paths(params, first_variance, innovations):
    """Path sums of negative raw returns squared, in decimal-return squared units.

innovations has shape (paths, horizon) and standardized unit-variance draws.
The state and mean use percent units, matching arch's fitted parameters.
"""
    z = np.asarray(innovations, dtype=float)
    if z.ndim != 2 or z.shape[1] < 1 or not np.isfinite(z).all():
        raise ValueError('Need finite path-by-horizon innovations')
    if not np.isfinite(first_variance) or first_variance <= 0:
        raise ValueError('Need positive first-step variance')
    h = np.full(z.shape[0], first_variance, dtype=float)
    losses = np.zeros(z.shape[0])
    for k in range(z.shape[1]):
        shock = np.sqrt(h) * z[:, k]
        r = (params['mu'] + shock) / 100
        losses += np.minimum(r, 0)**2
        h = (params['omega'] + params['alpha[1]'] * shock**2
             + params['gamma[1]'] * shock**2 * (shock < 0)
             + params['beta[1]'] * h)
    return losses


def fixed_gjr_forecasts(observed_after_fit, params, last_training_return,
                        last_training_variance, training_date,
                        horizon=5, paths=20000, seed=42):
    """Forecast at training close and subsequent closes, never reading ahead.

Date-keyed RNGs ensure extending/changing future data cannot alter old draws.
SE is simulation error conditional on the fitted model, not forecast uncertainty.
"""
    validate_series(observed_after_fit)
    if observed_after_fit.isna().any() or observed_after_fit.index.min() <= pd.Timestamp(training_date):
        raise ValueError('Post-fit observations must be complete and after training')
    if params['nu'] <= 2 or paths < 2 or horizon < 1:
        raise ValueError('Need nu > 2, at least two paths, and positive horizon')
    origins = pd.concat([pd.Series([last_training_return], index=[pd.Timestamp(training_date)]),
                         observed_after_fit])
    h = float(last_training_variance)
    rows = []
    for date, r in origins.items():
        # h is the variance of the return just observed on date.
        h_next = float(next_variance(params, float(r)*100-params['mu'], h))
        rng = np.random.default_rng(np.random.SeedSequence([seed, date.toordinal()]))
        z = rng.standard_t(params['nu'], size=(paths, horizon))
        z *= np.sqrt((params['nu']-2)/params['nu'])
        losses = gjr_downside_paths(params, h_next, z)
        rows.append({'Date': date, 'next_variance_percent_squared': h_next,
                     'downside_5d_forecast': losses.mean(),
                     'monte_carlo_se': losses.std(ddof=1)/np.sqrt(paths)})
        h = h_next
    return pd.DataFrame(rows).set_index('Date')


def risk_allocation(score, window=252, quantile=.8, high_weight=.5, normal_weight=1.):
    """Use previous scores only; warmup has no target rather than implicit trading."""
    validate_series(score)
    if window < 2 or not 0 < quantile < 1 or not 0 <= high_weight <= normal_weight <= 1:
        raise ValueError('Invalid allocation configuration')
    if score.isna().any() or (score < 0).any():
        raise ValueError('Scores must be complete and nonnegative')
    threshold = score.shift(1).rolling(window, min_periods=window).quantile(quantile)
    high = score > threshold
    target = pd.Series(np.where(high, high_weight, normal_weight), index=score.index)
    target = target.where(threshold.notna())
    return pd.DataFrame({'score':score, 'threshold':threshold, 'target_weight':target})


def rebalance(stock, cash, target, cost_rate):
    """Solve transaction cost and desired post-cost weight simultaneously."""
    if not 0 <= target <= 1 or not 0 <= cost_rate < 1 or min(stock, cash) < -1e-12:
        raise ValueError('Long-only weights, nonnegative holdings and valid cost required')
    wealth = stock+cash
    gap = target*wealth-stock
    trade = gap/(1+cost_rate*target) if gap >= 0 else gap/(1-cost_rate*target)
    fee = abs(trade)*cost_rate
    return stock+trade, cash-trade-fee, abs(trade), fee


def portfolio_ledger(returns, signals, evaluation_start, cost_bps=5, cash_return=0.):
    """Signals at close t are executed at close t+1; subsequent returns earn them.

First row is initial entry from cash, with costs but no SPY return. Last row
liquidates after earning that day's return. Adjusted-price returns represent
an idealized divisible total-return SPY holding (dividends reinvested).
"""
    validate_series(returns)
    if returns.isna().any() or (returns <= -1).any() or not np.isfinite(cash_return) or cash_return <= -1:
        raise ValueError('Invalid complete asset returns')
    if signals.index.has_duplicates or not signals.index.is_monotonic_increasing:
        raise ValueError('Invalid signal index')
    targets = signals.reindex(returns.index).shift(1)
    origin = pd.Series(returns.index, index=returns.index).shift(1)
    dates = returns.index[returns.index >= pd.Timestamp(evaluation_start)]
    if len(dates) < 2 or targets.loc[dates].isna().any():
        raise ValueError('Need two evaluation dates and fully calibrated prior signals')
    stock, cash = 0., 1.
    rows=[]
    for i, date in enumerate(dates):
        previous = stock+cash
        weight_start = stock/previous
        market_return = 0. if i == 0 else float(returns.loc[date])
        stock *= 1+market_return
        cash *= 1+(0. if i == 0 else cash_return)
        before_trade = stock+cash
        drifted_weight = stock/before_trade
        target = 0. if i == len(dates)-1 else float(targets.loc[date])
        stock,cash,turnover,fee = rebalance(stock,cash,target,cost_bps/10000)
        wealth=stock+cash
        rows.append({'Date':date,'signal_date':origin.loc[date],
                     'market_return':market_return,'weight_earning_return':weight_start,
                     'weight_before_trade':drifted_weight,'executed_target':target,
                     'turnover_fraction':turnover/before_trade,'fee_fraction':fee/before_trade,
                     'fee_per_initial_dollar':fee,'stock_value':stock,'cash_value':cash,
                     'wealth':wealth,'net_return':wealth/previous-1})
    ledger=pd.DataFrame(rows).set_index('Date')
    ledger['drawdown']=ledger.wealth/ledger.wealth.cummax().clip(lower=1)-1
    return ledger


def performance(ledger):
    years=(ledger.index[-1]-ledger.index[0]).days/365.25
    if years <= 0:
        raise ValueError('Need a positive evaluation interval')
    terminal=float(ledger.wealth.iloc[-1])
    return {'net_total_return':terminal-1,'cagr':terminal**(1/years)-1,
            'annualized_volatility':ledger.net_return.iloc[1:].std(ddof=1)*np.sqrt(252),
            'max_drawdown':ledger.drawdown.min(),
            'average_exposure':ledger.weight_earning_return.iloc[1:].mean(),
            'annual_turnover':ledger.turnover_fraction.sum()/years,
            'cost_dollars_per_10000':ledger.fee_per_initial_dollar.sum()*10000,
            'terminal_dollars_per_10000':terminal*10000}
