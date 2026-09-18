import numpy as np
import pandas as pd
import pytest
from left_tail.backtest import (gjr_downside_paths, fixed_gjr_forecasts,
                               risk_allocation, rebalance, portfolio_ledger, performance)

P={'omega':.1,'alpha[1]':.05,'gamma[1]':.1,'beta[1]':.8,'mu':.1,'nu':8.}

def test_downside_uses_raw_mean_shifted_returns_and_decimal_units():
    values=gjr_downside_paths(P,1.,np.array([[-1.],[1.],[0.]]))
    np.testing.assert_allclose(values,[.009**2,0,0])

def test_multistep_simulation_updates_negative_shock_state():
    p=dict(P,mu=0)
    # First shock -2 at variance 1 -> next variance .1+.05*4+.1*4+.8=1.5
    values=gjr_downside_paths(p,1.,np.array([[-2.,-1.]]))
    assert values[0]==pytest.approx((4+1.5)/10000)

def test_future_data_cannot_change_past_forecasts():
    r=pd.Series([.01,-.02,.03,.04],index=pd.bdate_range('2020-01-02',periods=4))
    a=fixed_gjr_forecasts(r,P,0.,1.,'2019-12-31',paths=100)
    changed=r.copy();changed.iloc[2:]=[-.5,.6]
    b=fixed_gjr_forecasts(changed,P,0.,1.,'2019-12-31',paths=100)
    pd.testing.assert_frame_equal(a.iloc[:3],b.iloc[:3])
    shorter=fixed_gjr_forecasts(r.iloc[:2],P,0.,1.,'2019-12-31',paths=100)
    pd.testing.assert_frame_equal(a.iloc[:3],shorter)

def test_zero_mean_one_step_simulation_matches_half_variance():
    p=dict(P,mu=0)
    rng=np.random.default_rng(9)
    z=rng.standard_t(8,size=(100000,1))*np.sqrt(6/8)
    x=gjr_downside_paths(p,4.,z)
    assert abs(x.mean()-.5*4/10000) < 5*x.std(ddof=1)/np.sqrt(len(x))

def test_threshold_excludes_today_and_has_full_warmup():
    s=pd.Series([1.,2.,3.,100.],index=pd.bdate_range('2020-01-01',periods=4))
    a=risk_allocation(s,window=3,quantile=.5)
    assert a.target_weight.iloc[:3].isna().all()
    assert a.threshold.iloc[3]==2
    assert a.target_weight.iloc[3]==.5

def test_costs_exact_post_cost_weights_and_self_financing():
    for s,c,w in [(0.,1.,1.),(.7,.3,.5),(.2,.8,.5),(1.,0.,0.)]:
        ns,nc,traded,fee=rebalance(s,c,w,.001)
        assert ns+nc==pytest.approx(s+c-fee)
        assert ns/(ns+nc)==pytest.approx(w)
        assert fee==pytest.approx(traded*.001)
        assert min(ns,nc)>=-1e-12

def test_signal_does_not_avoid_return_before_execution():
    dates=pd.bdate_range('2021-01-01',periods=5)
    r=pd.Series([0.,0.,-.2,.1,0.],index=dates)
    signal=pd.Series([1.,0.,1.,1.,1.],index=dates)
    l=portfolio_ledger(r,signal,dates[1],cost_bps=0)
    assert l.loc[dates[2],'weight_earning_return']==1
    assert l.loc[dates[2],'net_return']==pytest.approx(-.2)
    assert l.loc[dates[3],'weight_earning_return']==0
    assert l.loc[dates[3],'net_return']==0
    assert l.loc[dates[2],'signal_date']==dates[1]

def test_buy_hold_cash_entry_exit_costs_and_compounding():
    dates=pd.bdate_range('2021-01-01',periods=4)
    r=pd.Series([0.,.1,.1,-.1],index=dates)
    full=pd.Series(1.,index=dates)
    l=portfolio_ledger(r,full,dates[1],cost_bps=10)
    assert l.wealth.iloc[-1]==pytest.approx(1/(1+.001)*1.1*.9*(1-.001))
    assert l.wealth.iloc[-1]==pytest.approx((1+l.net_return).prod())
    c=portfolio_ledger(r,full*0,dates[1],cost_bps=10,cash_return=.001)
    assert c.wealth.iloc[-1]==pytest.approx(1.001**2)
    assert c.fee_fraction.sum()==0

def test_constant_weight_charges_for_market_drift():
    dates=pd.bdate_range('2021-01-01',periods=4)
    r=pd.Series([0.,0.,.2,0.],index=dates)
    l=portfolio_ledger(r,pd.Series(.5,index=dates),dates[1],cost_bps=10)
    assert l.weight_before_trade.iloc[1]>.5
    assert l.turnover_fraction.iloc[1]>0
    assert l.executed_target.iloc[1]==.5

def test_metrics_include_initial_wealth_in_drawdown():
    dates=pd.bdate_range('2021-01-01',periods=4)
    r=pd.Series(0.,index=dates)
    l=portfolio_ledger(r,pd.Series(1.,index=dates),dates[1],cost_bps=10)
    p=performance(l)
    assert p['max_drawdown']==pytest.approx(l.wealth.iloc[-1]-1)
    assert p['average_exposure']==1

def test_missing_prior_signal_fails_instead_of_silent_fill():
    dates=pd.bdate_range('2021-01-01',periods=4)
    with pytest.raises(ValueError):
        portfolio_ledger(pd.Series(0.,index=dates),pd.Series(np.nan,index=dates),dates[1])
