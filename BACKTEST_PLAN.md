# Economic-value experiment

Added 2026-09-18 at the author's request. This is a research backtest of a simple SPY/cash allocation, not a recommendation or a claim of profitability. It expands the original plan's forecasting-only scope. The author subsequently requested the backtest in Part 1. The first run is now implemented in Notebook 01 and `scripts/run_backtest.py`, using settings recorded in `config/part1_backtest.json` before strategy outcomes were inspected.

## Question and scope

Does reducing SPY exposure when forecast downside risk is high improve the return/risk tradeoff after trading costs, compared with simple alternatives?

Each article ends with a conclusion stating what was established, what was not, and what the next experiment tests. Part 1 now includes model foundations and a narrow, fixed-parameter five-session downside-forecast allocation pilot. Part 2 retains the broader forecast-target and accuracy study. Parts 3–5 apply the same allocation rule to the new models; Parts 6–7 compare and summarize them. Do not fabricate a Part 1 out-of-sample result from full-training fitted paths.

## Recorded allocation rule

- Hold 100% SPY in the normal-risk state and 50% SPY / 50% cash in the high-risk state. No leverage or shorting.
- Define high risk as a five-session downside-risk forecast above the 80th percentile of the previous 252 valid historical forecasts, excluding today's forecast. Use only forecasts produced with information then available. Require a complete calibration window before evaluation.
- Review the signal daily. Use identical decision logic across models; change only the forecast source. A percentile of downside variance gives the same ordering as a percentile of its square root.
- **Heuristics:** the 50% exposure, 80th percentile, and 252-session window are practical design choices, not mathematical optima or evidence-based guarantees. They are starting defaults, not values selected for the best test performance.

## Information and execution timing

- Parameters, features, scaling, target observations, and calibration thresholds must be available at the forecast timestamp. Five-session training labels must have fully matured before they can be used.
- Retain the primary forecast target for sessions t+1 through t+5. Document the GJR conversion from total conditional variance to expected squared negative raw returns; do not silently rename total variance as downside variance.
- With close-only inputs, form the signal after close t, execute at close t+1, and apply the new exposure to returns from close t+1 onward. Never credit that signal with avoiding the return from t to t+1. This deliberately delayed execution misses the first session of the five-session prediction window; report that mismatch explicitly.
- Track positions and cash through time. Charge turnover against the position after market movement, not simply the difference between successive target weights. Include entry, daily rebalancing where required, and liquidation at the final evaluation close, including costs.

## Evaluation and comparisons

- Preserve chronological development, calibration, and final evaluation periods. Set exact boundaries and refit schedules before generating the first strategy results. The pilot fits through 2019-12-31, freezes parameters without refitting, uses 2020 forecasts for threshold warmup, enters at the 2021-01-04 close, and earns returns from 2021-01-05 through 2026-09-15. The 2020 crash is excluded from portfolio evaluation; 2021 and 2026 are partial calendar-year performance rows.
- Remove training labels whose future windows cross a validation/test boundary. Overlapping five-day labels are not independent observations.
- Freeze rules and model-selection procedures before reporting the common final test period. Do not tune later installments using earlier published final-test results. Any change informed by those results becomes exploratory and needs a new evaluation period.
- Compare against buy-and-hold SPY, daily-rebalanced 50% SPY / 50% cash, and the same signal rule driven by a trailing historical downside-risk baseline. Report average exposure so a lower drawdown from simply owning less SPY is visible.
- Primary trading cost: 5 basis points per dollar of SPY traded, with predeclared 0 and 10 basis point scenarios. These are cost assumptions, not verified execution quotes. One basis point is 0.01%.
- Initially use zero cash interest and label that assumption. Before interpreting net economic value, also assess an appropriately dated cash-rate series with documented source and conventions. Apply the same cash assumptions to every comparator; do not treat a quoted annual yield as a realized daily return.
- Report compounded net return/CAGR, annualized daily volatility, maximum drawdown, turnover, costs, and average SPY exposure on identical dates. If reporting Sharpe ratios, define and align the risk-free series. Include missed rebounds and subperiod behavior, not only avoided losses.
- Separate forecast accuracy, allocation performance, and any statistical uncertainty. Lower forecast error does not automatically imply better investment outcomes. Do not multiply overlapping five-day strategy returns to create a wealth curve; use the daily portfolio ledger.

## Reproducibility and validity checks

Save dated forecasts, signal thresholds, target/executed weights, turnover, costs, cash returns, daily portfolio returns, and all protocol settings. Preserve input hashes, seeds, versions, and the existing frozen-data limitation.

Test information timing and delayed execution, label maturity and split boundaries, weight drift and cash accounting, transaction costs, all-SPY/all-cash limiting cases, and wealth compounding on small known examples. Compare models on common eligible dates after their warmup periods.

Forecast implementation reference: https://arch.readthedocs.io/en/latest/univariate/forecasting.html

## Recorded pilot outcome and limits

At 5 basis points, GJR's CAGR is 12.87%, maximum drawdown -19.66%, and average SPY exposure 89.65%. Buy-and-hold earns 14.94% with a -24.50% drawdown. The historical downside signal earns 13.36% with a -20.15% drawdown at 89.62% exposure. The model does not demonstrate a return advantage over either comparator. See `results/backtest/metrics.csv` for all cost scenarios and the notebook for interpretation. No tuning was performed after these outcomes appeared.

The forecast is a 20,000-path Monte Carlo average of five-session squared negative raw returns, retaining the fitted mean and Student-t variance normalization. Seeds are date-specific and repeatable. Median relative simulation SE is approximately 1.3%; this quantifies only numerical sampling error. No forward realized labels are used for fitting or calibration, so forward-label boundary purging is reserved for the later supervised experiments.

The observed 2021–2026 evaluation period cannot be treated as newly untouched after using these results to change the design. Future outcome-informed revisions must be labeled exploratory or evaluated on new data. Cash earns zero in this pilot; the cash-rate sensitivity and parameter/model uncertainty studies are still pending.
