"""Reproduce Part 1 from the saved snapshot, without running notebook cells."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.uv-cache/matplotlib'))
import hashlib
import json
import time
import shutil
import numpy as np
import pandas as pd
from left_tail.data import daily_returns
from left_tail.targets import daily_variance, daily_downside_variance
from left_tail.validation import chronological_split
from left_tail.garch import fit_models, persistence, shock_table
from left_tail.plots import plot_shock_responses, plot_training_volatility

TRAIN_END = '2019-12-31'


def main():
    np.random.seed(42)
    raw = ROOT / 'data/raw'
    manifest = json.loads((raw / 'manifest.json').read_text())
    for filename, expected in manifest['sha256'].items():
        if hashlib.sha256((raw / filename).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f'Snapshot checksum mismatch: {filename}')
    prices = pd.read_csv(raw / 'SPY_source.csv', index_col='Date', parse_dates=True)['Adj Close']
    returns = daily_returns(prices)
    if returns.iloc[1:].isna().any():
        raise ValueError('Unexpected missing SPY returns; investigate before dropping dates')
    returns = returns.iloc[1:]
    train, holdout = chronological_split(returns, TRAIN_END)
    begin = time.perf_counter()
    fits, diagnostics = fit_models(train)
    elapsed = time.perf_counter() - begin
    tables, figures = ROOT / 'results/tables', ROOT / 'results/figures'
    tables.mkdir(parents=True, exist_ok=True); figures.mkdir(parents=True, exist_ok=True)
    params = pd.DataFrame({name: fit.params for name, fit in fits.items()}).T
    params.index.name = 'model'
    params.to_csv(tables / 'garch_parameters.csv')
    rows = []
    for name, fit in fits.items():
        rows.append({'model': name, 'training_observations': int(fit.nobs),
                     'reserved_test_observations': len(holdout), 'parameter_count': len(fit.params),
                     'persistence': persistence(fit.params), 'aic_in_sample': fit.aic,
                     'log_likelihood_in_sample': fit.loglikelihood,
                     'convergence_flag': int(fit.convergence_flag)})
    pd.DataFrame(rows).to_csv(tables / 'model_summary.csv', index=False)
    # Identical starting state isolates response curves; estimated on training data only.
    prior_variance = float((train * 100).var(ddof=0))
    shocks = shock_table(fits, prior_variance)
    shocks.to_csv(tables / 'shock_responses.csv', index=False)
    summary = {'total_prices': len(prices), 'total_returns': len(returns), 'train_n': len(train),
               'reserved_test_n': len(holdout), 'train_start': str(train.index.min().date()),
               'train_end': str(train.index.max().date()), 'test_start': str(holdout.index.min().date()),
               'test_end': str(holdout.index.max().date()), 'fit_runtime_seconds': elapsed,
               'shock_prior_variance_percent_squared': prior_variance,
               'seed': 42, 'mean_model': 'estimated constant', 'return_definition': 'simple adjusted-close returns',
               'return_input_units': 'percent for arch; decimal for daily target calculations',
               'diagnostics': diagnostics,
               'scope': 'Part 1 training fits only. Holdout outcomes not evaluated. No forward targets or predictions.'}
    (tables / 'part1_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    # Save only training observations/paths here; holdout is reserved for later phases.
    daily = pd.concat([train, daily_variance(train), daily_downside_variance(train)], axis=1)
    daily.to_csv(tables / 'training_daily_measures.csv', index_label='Date')
    plot_shock_responses(shocks, prior_variance, figures / 'shock_responses.png')
    plot_training_volatility(train, fits, figures / 'training_volatility.png')
    for filename in ['shock_responses.png', 'training_volatility.png']:
        shutil.copyfile(figures / filename, ROOT / 'article/figures' / filename)
    print(json.dumps(summary, indent=2))
    print(params.to_string())
    if any(d['convergence_flag'] != 0 for d in diagnostics):
        raise RuntimeError('A fit did not converge; review diagnostics before treating Part 1 as complete')


if __name__ == '__main__':
    main()
