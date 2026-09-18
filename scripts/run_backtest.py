"""Run the frozen Part 1 SPY/cash experiment from checksum-verified local data."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.uv-cache/matplotlib'))
import argparse
import hashlib
import json
import platform
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import arch
import scipy
import exchange_calendars as xcals
from arch import arch_model
from left_tail.data import daily_returns
from left_tail.backtest import fixed_gjr_forecasts,risk_allocation,portfolio_ledger,performance


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=ROOT/'results/backtest')
    args=parser.parse_args()
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    config_path=ROOT/'config/part1_backtest.json'
    cfg=json.loads(config_path.read_text())
    raw=ROOT/'data/raw/SPY_source.csv'
    reference=json.loads((ROOT/'results/tables/data_manifest.json').read_text())
    actual=hashlib.sha256(raw.read_bytes()).hexdigest()
    if actual != reference['sha256']['SPY_source.csv']:
        raise RuntimeError('SPY differs from the committed reference snapshot')
    prices=pd.read_csv(raw,index_col='Date',parse_dates=True)['Adj Close']
    calendar=xcals.get_calendar('XNYS',start=prices.index.min(),end=prices.index.max())
    expected=calendar.sessions_in_range(prices.index.min(),prices.index.max()).tz_localize(None)
    if not prices.index.equals(expected):
        raise ValueError('SPY dates do not match the expected session calendar')
    returns=daily_returns(prices).iloc[1:]
    if returns.isna().any():raise ValueError('Missing returns')
    train=returns.loc[:cfg['train_end']]
    observed=returns.loc[returns.index>train.index[-1]]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        fit=arch_model(100*train,mean='Constant',vol='GARCH',p=1,o=1,q=1,
                       dist='StudentsT',rescale=False).fit(disp='off',options={'maxiter':2000})
    if fit.convergence_flag:raise RuntimeError('GJR fit failed to converge')
    print('Forecasting five-session downside risk with frozen pre-2020 parameters...',flush=True)
    forecasts=fixed_gjr_forecasts(observed,fit.params,float(train.iloc[-1]),
        float(fit.conditional_volatility.iloc[-1]**2),train.index[-1],
        horizon=cfg['forecast_horizon'],paths=cfg['simulation_paths'],seed=cfg['seed'])
    forecasts['historical_downside_5d']=(np.minimum(returns,0)**2).rolling(
        cfg['baseline_window'],min_periods=cfg['baseline_window']).mean().reindex(forecasts.index)*cfg['forecast_horizon']
    allocation_args=dict(window=cfg['threshold_window'],quantile=cfg['high_risk_quantile'],
        high_weight=cfg['high_risk_exposure'],normal_weight=cfg['normal_exposure'])
    gjr=risk_allocation(forecasts.downside_5d_forecast,**allocation_args)
    hist=risk_allocation(forecasts.historical_downside_5d,**allocation_args)
    signals=pd.DataFrame({'GJR downside rule':gjr.target_weight,
                          'Historical downside rule':hist.target_weight,
                          'Buy and hold SPY':1.,'Fixed 50% SPY / 50% cash':.5},index=forecasts.index)
    thresholds=pd.DataFrame({'gjr_threshold':gjr.threshold,'historical_threshold':hist.threshold},index=forecasts.index)
    metrics=[];ledgers=[];annual=[];primary={}
    for cost in cfg['cost_scenarios_bps']:
        for name in signals:
            ledger=portfolio_ledger(returns,signals[name],cfg['evaluation_start'],
                                    cost_bps=cost,cash_return=cfg['cash_daily_return'])
            metrics.append({'strategy':name,'cost_bps':cost,**performance(ledger)})
            if cost==cfg['primary_cost_bps']:
                primary[name]=ledger
                ledgers.append(ledger.assign(strategy=name))
                for year,group in ledger.groupby(ledger.index.year):
                    annual.append({'strategy':name,'year':year,'net_return':(1+group.net_return).prod()-1,
                                   'average_exposure':group.weight_earning_return.iloc[1:].mean()
                                      if year==ledger.index[0].year else group.weight_earning_return.mean(),
                                   'partial_year':bool(year in (ledger.index[0].year, ledger.index[-1].year))})
    forecasts.to_csv(out/'forecasts.csv',index_label='Date')
    signals.join(thresholds).to_csv(out/'signals.csv',index_label='Date')
    pd.concat(ledgers).to_csv(out/'daily_ledger.csv',index_label='Date')
    summary=pd.DataFrame(metrics)
    summary.to_csv(out/'metrics.csv',index=False)
    pd.DataFrame(annual).to_csv(out/'annual_returns.csv',index=False)
    fit.params.to_json(out/'parameters.json',indent=2)
    sample=next(iter(primary.values()))
    metadata={'config':cfg,'config_sha256':hashlib.sha256(config_path.read_bytes()).hexdigest(),
      'SPY_sha256':actual,'training_returns':len(train),'training_start':str(train.index[0].date()),
      'training_end':str(train.index[-1].date()),'entry_date':str(sample.index[0].date()),
      'first_earned_return_date':str(sample.index[1].date()),'last_date':str(sample.index[-1].date()),
      'evaluation_return_intervals':len(sample)-1,'threshold_calibration':'2020 forecasts; no portfolio evaluation in 2020',
      'convergence_flag':int(fit.convergence_flag),'fit_warnings':[str(w.message) for w in caught],
      'median_relative_mc_se':float((forecasts.monte_carlo_se/forecasts.downside_5d_forecast).median()),
      'versions':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,
                  'arch':arch.__version__,'scipy':scipy.__version__,'exchange_calendars':xcals.__version__},
      'limitations':['Single historical out-of-sample pilot; not an untouched future evaluation after publication.',
        'No parameter tuning on strategy results; GJR selected in the research plan.',
        'Zero cash interest; taxes and market impact omitted; fixed proportional trading costs.',
        'Divisible total-return SPY exposure, using adjusted-close return proxy.',
        'One-close execution delay misses the first session of the forecast window.',
        'Monte Carlo estimates have sampling error; SE excludes parameter and model uncertainty.',
        '2020 crash excluded from portfolio evaluation; 2026 is a partial year.',
        'Frozen input data is local; distribution remains unresolved.']}
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    fig,axes=plt.subplots(3,1,figsize=(11,10),sharex=True,gridspec_kw={'height_ratios':[2,1.4,1]})
    colors={'GJR downside rule':'#147d92','Historical downside rule':'#c07931',
            'Buy and hold SPY':'#303f50','Fixed 50% SPY / 50% cash':'#929b9e'}
    for name,l in primary.items():
        axes[0].plot(l.index,l.wealth*10000,label=name,color=colors[name],lw=1.5)
        axes[1].plot(l.index,l.drawdown*100,color=colors[name],lw=1.2)
    axes[2].step(sample.index[1:],primary['GJR downside rule'].weight_earning_return.iloc[1:]*100,
                 where='pre',color=colors['GJR downside rule'],lw=.9)
    axes[0].set_ylabel('Portfolio value ($)');axes[0].legend(frameon=False,fontsize=9)
    axes[1].set_ylabel('Drawdown (%)');axes[2].set_ylabel('GJR exposure (%)')
    for ax in axes:
        ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
    fig.suptitle('SPY allocation pilot: out-of-sample performance\nFrozen 2019 fit; 2020 threshold warmup; evaluation from 2021',fontsize=14)
    fig.text(.5,.01,'5 bps per dollar traded, including entry/exit. Cash earns 0%. Signals execute at the following close. No leverage.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.035,1,.94))
    fig.savefig(out/'performance.png',dpi=180,bbox_inches='tight');plt.close(fig)
    print(summary.loc[summary.cost_bps==cfg['primary_cost_bps']].to_string(index=False),flush=True)
    print(json.dumps({k:metadata[k] for k in ['entry_date','first_earned_return_date','last_date','evaluation_return_intervals','median_relative_mc_se']},indent=2))

if __name__=='__main__':main()
