"""The four Part 1 models and their one-step shock responses."""
import warnings
import numpy as np
import pandas as pd
from arch import arch_model
from .data import validate_series

MODEL_SPECS = {
    'ARCH(1)': dict(vol='ARCH', p=1, dist='normal'),
    'GARCH(1,1)': dict(vol='GARCH', p=1, o=0, q=1, dist='normal'),
    'GARCH-t': dict(vol='GARCH', p=1, o=0, q=1, dist='StudentsT'),
    'GJR-GARCH-t': dict(vol='GARCH', p=1, o=1, q=1, dist='StudentsT'),
}


def fit_models(train):
    """Input decimal returns; fit in percent units with an estimated constant mean."""
    validate_series(train)
    if train.isna().any() or len(train) < 20 or train.std() == 0:
        raise ValueError('Need nonconstant, complete returns for fitting')
    results, diagnostics = {}, []
    for name, spec in MODEL_SPECS.items():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            result = arch_model(100 * train, mean='Constant', rescale=False, **spec).fit(
                disp='off', options={'maxiter': 2000})
        results[name] = result
        diagnostics.append({'model': name, 'convergence_flag': int(result.convergence_flag),
                            'warnings': [str(w.message) for w in caught]})
    return results, diagnostics


def next_variance(params, shock_percent, previous_variance):
    """One-step conditional variance, in percent-squared units. Shock = r - mu."""
    e = np.asarray(shock_percent, dtype=float)
    if not np.isfinite(e).all() or not np.isfinite(previous_variance) or previous_variance < 0:
        raise ValueError('Shock and previous variance must be finite; variance nonnegative')
    return (params['omega'] + params['alpha[1]'] * e**2
            + params.get('beta[1]', 0) * previous_variance
            + params.get('gamma[1]', 0) * e**2 * (e < 0))


def persistence(params):
    """Symmetric standardized errors: GJR persistence includes gamma/2."""
    return params['alpha[1]'] + params.get('beta[1]', 0) + params.get('gamma[1]', 0) / 2


def shock_table(results, previous_variance):
    rows = []
    for name, result in results.items():
        for shock in [-4., -2., -1., 1., 2., 4.]:
            variance = float(next_variance(result.params, shock, previous_variance))
            rows.append({'model': name, 'shock_percent': shock,
                         'next_variance_percent_squared': variance,
                         'next_daily_volatility_percent': np.sqrt(variance)})
    return pd.DataFrame(rows)
