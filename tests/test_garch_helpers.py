from types import SimpleNamespace
import numpy as np
import pandas as pd
import pytest
from left_tail.garch import next_variance, persistence, fit_models, shock_table

P = {'omega': .1, 'alpha[1]': .1, 'beta[1]': .8}


def test_known_recursion_and_symmetry():
    assert next_variance(P, 2., 1.) == pytest.approx(1.3)
    assert next_variance(P, -2., 1.) == pytest.approx(1.3)


def test_asymmetry_and_persistence():
    p = dict(P, **{'gamma[1]': .1})
    assert next_variance(p, -2., 1.) - next_variance(p, 2., 1.) == pytest.approx(.4)
    assert persistence(p) == pytest.approx(.95)
    assert persistence(P) == pytest.approx(.9)


def test_arch_has_no_previous_variance_term():
    p = {'omega': .1, 'alpha[1]': .2}
    assert next_variance(p, 1., 100.) == pytest.approx(.3)


def test_shock_table_units_and_levels():
    t = shock_table({'example': SimpleNamespace(params=P)}, 1.)
    assert set(t.shock_percent) == {-4, -2, -1, 1, 2, 4}
    np.testing.assert_allclose(t.next_daily_volatility_percent**2, t.next_variance_percent_squared)


def test_invalid_variance_rejected():
    with pytest.raises(ValueError):
        next_variance(P, 1., -1.)


def test_model_family_mean_units_and_parameter_counts():
    r = pd.Series(np.random.default_rng(3).normal(0, .01, 600), index=pd.date_range('2000-01-01', periods=600))
    fits, diagnostics = fit_models(r)
    assert [len(f.params) for f in fits.values()] == [3, 4, 5, 6]
    for fit in fits.values():
        np.testing.assert_allclose(fit.model.y, r * 100)
        assert 'mu' in fit.params
        assert fit.nobs == len(r)
        assert np.isfinite(fit.conditional_volatility).all()
    assert all(d['convergence_flag'] == 0 for d in diagnostics)
