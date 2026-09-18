"""Regenerate article charts from saved backtest CSVs; no fitting or simulation."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.uv-cache/matplotlib'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter

ORDER=['Buy and hold SPY','GJR downside rule','Historical downside rule','Fixed 50% SPY / 50% cash']
LABELS=['Buy-and-hold SPY','GJR downside rule','Historical downside rule','Fixed 50/50']
COLORS=['#34455c','#087f8c','#bd691e','#949da6']
FOOT='Entry: Jan 4, 2021 · End: Sep 15, 2026 · Cash earns 0% · 2020 is calibration only'


def finish(fig,name,foot=FOOT):
    fig.text(.08,.025,foot,fontsize=9,color='#4e5864')
    fig.tight_layout(rect=(0,.06,1,.93))
    fig.savefig(ROOT/'article/figures'/name,dpi=200,bbox_inches='tight',facecolor='white')
    plt.close(fig)


def main():
    folder=ROOT/'results/backtest'
    ledger=pd.read_csv(folder/'daily_ledger.csv',parse_dates=['Date']).set_index('Date')
    metrics=pd.read_csv(folder/'metrics.csv')
    annual=pd.read_csv(folder/'annual_returns.csv')
    primary=metrics.loc[metrics.cost_bps==5].set_index('strategy')
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    groups={name:ledger.loc[ledger.strategy==name] for name in ORDER}
    # Sanity checks prevent charts quietly disagreeing with the recorded metrics.
    reference=groups[ORDER[0]].index
    for name,g in groups.items():
        assert g.index.equals(reference)
        np.testing.assert_allclose(g.wealth.iloc[-1]*10000,primary.loc[name,'terminal_dollars_per_10000'])
        np.testing.assert_allclose(g.drawdown.min(),primary.loc[name,'max_drawdown'])
        np.testing.assert_allclose((1+g.net_return).prod(),g.wealth.iloc[-1])
    fig,axes=plt.subplots(2,1,figsize=(11,8),sharex=True)
    for name,label,color in zip(ORDER,LABELS,COLORS):
        g=groups[name]
        axes[0].plot(g.index,g.wealth*10000,label=f'{label}  (${g.wealth.iloc[-1]*10000:,.0f})',color=color,lw=1.7)
        axes[1].plot(g.index,g.drawdown,color=color,lw=1.3)
    axes[0].set_ylabel('Value of $10,000');axes[0].yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
    axes[0].legend(frameon=False,fontsize=9,loc='upper left')
    axes[1].set_ylabel('Decline from previous peak');axes[1].yaxis.set_major_formatter(PercentFormatter(1))
    for ax in axes:ax.grid(axis='y',alpha=.2)
    fig.suptitle('Less drawdown, but also less growth',fontsize=17,x=.08,ha='left')
    finish(fig,'backtest_growth_drawdown.png',FOOT+'\nNet of 5 bps per dollar traded, including entry and liquidation. Legend shows ending values.')

    years=sorted(annual.year.unique());x=np.arange(len(years));width=.19
    fig,ax=plt.subplots(figsize=(11,6))
    for j,(name,label,color) in enumerate(zip(ORDER,LABELS,COLORS)):
        rows=annual.loc[annual.strategy==name].set_index('year').loc[years]
        vals=rows.net_return.to_numpy()
        for year,value in zip(years,vals):
            g=groups[name];v=(1+g.loc[g.index.year==year,'net_return']).prod()-1
            np.testing.assert_allclose(value,v,atol=1e-12)
        bars=ax.bar(x+(j-1.5)*width,vals,width,label=label,color=color)
        ax.bar_label(bars,labels=[f'{v:.1%}' for v in vals],fontsize=8,padding=3)
    ax.axhline(0,color='#45515d',lw=.8);ax.set_xticks(x,[f'{y}*' if y in (years[0],years[-1]) else str(y) for y in years])
    ax.set_ylim(-.24,.40);ax.set_ylabel('Net return during year');ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.legend(frameon=False,ncol=2,fontsize=9,loc='upper right');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
    fig.suptitle('The tradeoff changes from year to year',fontsize=17,x=.08,ha='left')
    finish(fig,'backtest_annual_returns.png','5 bps per dollar traded · Cash earns 0%\n*2021 starts after the Jan 4 entry; 2026 ends Sep 15. These are partial-year returns, not annualized.')

    fig,axes=plt.subplots(1,2,figsize=(11,5.8),gridspec_kw={'width_ratios':[1.15,1]})
    for name,label,color in zip(ORDER,LABELS,COLORS):
        m=metrics.loc[metrics.strategy==name].sort_values('cost_bps')
        axes[0].plot(m.cost_bps,m.cagr,marker='o',label=label,color=color,lw=2)
    axes[0].set(xlabel='Cost per traded dollar (basis points)',ylabel='Net annualized return',xticks=[0,5,10])
    axes[0].yaxis.set_major_formatter(PercentFormatter(1));axes[0].legend(frameon=False,fontsize=8)
    axes[0].grid(axis='y',alpha=.2)
    values=primary.loc[ORDER,'annual_turnover'].to_numpy()
    bars=axes[1].barh(LABELS,values,color=COLORS)
    axes[1].bar_label(bars,labels=[f'{v:.2f}×' for v in values],padding=4)
    axes[1].invert_yaxis();axes[1].set_xlabel('Portfolio-equivalents traded per year');axes[1].set_xlim(0,max(values)*1.2)
    fig.suptitle('More trading makes GJR more sensitive to costs',fontsize=17,x=.08,ha='left')
    finish(fig,'backtest_cost_sensitivity.png','Same fixed strategy rules in all cost scenarios · Cash earns 0%\nTurnover uses the 5 bps ledger; one-way traded value / current wealth, including entry and exit.')

    signals=pd.read_csv(folder/'signals.csv',index_col='Date',parse_dates=True)
    forecasts=pd.read_csv(folder/'forecasts.csv',index_col='Date',parse_dates=True)
    ratio=(forecasts.downside_5d_forecast/signals.gjr_threshold).reindex(reference)
    fig,axes=plt.subplots(2,1,figsize=(11,6.8),sharex=True)
    axes[0].plot(ratio.index,ratio,color=COLORS[1],lw=.9)
    axes[0].axhline(1,color='#444',ls='--',lw=1,label='Threshold: ratio = 1')
    axes[0].set_yscale('log');axes[0].set_ylabel('Forecast / prior risk threshold\n(log scale)');axes[0].legend(frameon=False,fontsize=9)
    for name,label,color in zip(ORDER[1:3],LABELS[1:3],COLORS[1:3]):
        g=groups[name].iloc[1:]
        # Plot at each month's last observed date, avoiding a date after the sample.
        monthly=g.groupby(g.index.to_period('M')).agg(exposure=('weight_earning_return','mean'))
        dates=g.groupby(g.index.to_period('M')).apply(lambda z:z.index[-1])
        axes[1].plot(pd.DatetimeIndex(dates),monthly.exposure,label=label,color=color,lw=1.6,marker='.',ms=3)
    axes[1].set_ylim(.45,1.05);axes[1].set_ylabel('Mean SPY exposure\nby observed month');axes[1].yaxis.set_major_formatter(PercentFormatter(1))
    axes[1].legend(frameon=False,fontsize=9)
    for ax in axes:ax.grid(axis='y',alpha=.2)
    fig.suptitle('When did the rules reduce SPY exposure?',fontsize=17,x=.08,ha='left')
    finish(fig,'backtest_exposure.png','Above 1: signal requests 50% SPY; otherwise 100%. Signal executes at the following close.\nExposure is averaged by month for readability; Jan 2021 and Sep 2026 are partial months.')
    print('Generated 4 article charts; saved-metric and annual-ledger consistency checks passed.')

if __name__=='__main__':main()
