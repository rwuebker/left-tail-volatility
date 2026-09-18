# Economic-value experiment

Added 2026-09-18 at the author's request. This is a research backtest of a simple SPY/cash allocation, not a recommendation or a claim of profitability. It expands the original plan's forecasting-only scope. The rules below are proposed defaults to freeze before inspecting strategy results; no strategy results exist yet.

## Question and scope

Does reducing SPY exposure when forecast downside risk is high improve the return/risk tradeoff after trading costs, compared with simple alternatives?

Each article ends with a conclusion stating what was established, what was not, and what the next experiment tests. Part 1 establishes model foundations only. The first downside-driven strategy backtest belongs in Part 2, once genuine historical forecasts and the downside target exist. Parts 3–5 apply the same allocation rule to the new models; Parts 6–7 compare and summarize them. Do not fabricate a Part 1 out-of-sample result from full-training fitted paths.

## Proposed allocation rule

- Hold 100% SPY in the normal-risk state and 50% SPY / 50% cash in the high-risk state. No leverage or shorting.
- Define high risk as a five-session downside-risk forecast above the 80th percentile of the previous 252 valid historical forecasts, excluding today's forecast. Use only forecasts produced with information then available. Require a complete calibration window before evaluation.
- Review the signal daily. Use identical decision logic across models; change only the forecast source. A percentile of downside variance gives the same ordering as a percentile of its square root.
- **Heuristics:** the 50% exposure, 80th percentile, and 252-session window are practical design choices, not mathematical optima or evidence-based guarantees. They are starting defaults, not values selected for the best test performance.

## Information and execution timing

- Parameters, features, scaling, target observations, and calibration thresholds must be available at the forecast timestamp. Five-session training labels must have fully matured before they can be used.
- Retain the primary forecast target for sessions t+1 through t+5. Document the GJR conversion from total conditional variance to expected squared negative raw returns; do not silently rename total variance as downside variance.
- With close-only inputs, form the signal after close t, execute at close t+1, and apply the new exposure to returns from close t+1 onward. Never credit that signal with avoiding the return from t to t+1. This deliberately delayed execution misses the first session of the five-session prediction window; report that mismatch explicitly.
- Track positions and cash through time. Charge turnover against the position after market movement, not simply the difference between successive target weights. Include entry, daily rebalancing where required, and a documented terminal-position convention.

## Evaluation and comparisons

- Preserve chronological development, calibration, and final evaluation periods. Set exact boundaries and refit schedules before generating the first strategy results. Use the existing pre-2020 training cutoff as the starting point; a portion of later history may be needed for validation/calibration and must then be excluded from final evaluation.
- Remove training labels whose future windows cross a validation/test boundary. Overlapping five-day labels are not independent observations.
- Freeze rules and model-selection procedures before reporting the common final test period. Do not tune later installments using earlier published final-test results. Any change informed by those results becomes exploratory and needs a new evaluation period.
- Compare against buy-and-hold SPY, daily-rebalanced 50% SPY / 50% cash, and the same signal rule driven by a trailing historical downside-risk baseline. Report average exposure so a lower drawdown from simply owning less SPY is visible.
- Proposed primary trading cost: 5 basis points per dollar of SPY traded, with predeclared 0 and 10 basis point scenarios. These are cost assumptions, not verified execution quotes. One basis point is 0.01%.
- Initially use zero cash interest and label that assumption. Before interpreting net economic value, also assess an appropriately dated cash-rate series with documented source and conventions. Apply the same cash assumptions to every comparator; do not treat a quoted annual yield as a realized daily return.
- Report compounded net return/CAGR, annualized daily volatility, maximum drawdown, turnover, costs, and average SPY exposure on identical dates. If reporting Sharpe ratios, define and align the risk-free series. Include missed rebounds and subperiod behavior, not only avoided losses.
- Separate forecast accuracy, allocation performance, and any statistical uncertainty. Lower forecast error does not automatically imply better investment outcomes. Do not multiply overlapping five-day strategy returns to create a wealth curve; use the daily portfolio ledger.

## Reproducibility and validity checks

Save dated forecasts, signal thresholds, target/executed weights, turnover, costs, cash returns, daily portfolio returns, and all protocol settings. Preserve input hashes, seeds, versions, and the existing frozen-data limitation.

Test information timing and delayed execution, label maturity and split boundaries, weight drift and cash accounting, transaction costs, all-SPY/all-cash limiting cases, and wealth compounding on small known examples. Compare models on common eligible dates after their warmup periods.

Forecast implementation reference: https://arch.readthedocs.io/en/latest/univariate/forecasting.html
