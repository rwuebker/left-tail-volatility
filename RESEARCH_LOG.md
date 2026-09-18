# Research log

## 2026-09-16 — Part 1 environment setup (UTC)

- **Question:** Which installed Python should run the initial research?
- **Model / change:** Initialize a dedicated Git repository and uv-managed environment. Select Python 3.11.14, the installed native arm64 interpreter; default Python 3.14.5 and installed Python 3.12.13 run as x86_64.
- **Data used:** None yet.
- **Training sample size:** Not applicable; no data downloaded.
- **Result:** Python 3.11.14 arm64 verified. uv 0.12.15 installed locally; 87 packages installed and pinned in uv.lock. All 11 package import checks succeeded, and a locked offline sync succeeded. No research calculation tests exist yet.
- **Interpretation:** This is infrastructure setup, not an experiment. Dependency import checks do not establish scientific correctness.
- **Next step:** Download and audit SPY, VIX, and VIX3M if available; implement and test daily returns and downside variance. Continue only within Part 1 until review.

## Article opening — initial narrative draft

- **Question:** How do we invite the reader into the research without presuming an answer?
- **Model / change:** Draft sections 1–8 around equal positive and negative moves, the downside target, model memory, asymmetry, and extreme surprises. Keep each model attached to a question it helps investigate.
- **Data used / training sample size:** None; explanations only.
- **Result:** Opening draft written with primary documentation links; later sections remain explicitly unfinished.
- **Interpretation:** No empirical claims or model winners. The reader should discover the questions with us.
- **Next step:** Review the voice; add the actual data audit and model evidence as Part 1 progresses.

## Article voice revision

- **Change:** Revised the opening to sound conversational and exploratory, following the author's feedback. Removed declarations about the research philosophy and reduced rhetorical questions.
- **Result:** Sections 1–8 retain their definitions and sources; no empirical claims added.

## 2026-09-16 — Part 1 supporting implementation and guided notebook

- **Question:** How do squared returns differ from mean-centered shocks, and how do the four models respond to opposite shocks?
- **Model / change:** Added return/downside helpers, chronological split, four constant-mean model fits, and shock response helpers with tests. Added the mean/variance distinction to the article. Created the first notebook as a guided outline with context and unexecuted code prompts.
- **Data used:** Frozen SPY adjusted-close and VIX close history from Yahoo Finance. Yahoo VIX3M returned one row; Cboe CSV supplied 4,273 observations from 2009-09-18 to 2026-09-15. Source hashes and missing counts are in results/tables/data_manifest.json. The first SPY download was refreshed while finalizing the fallback; final checksums identify the snapshot used for fits.
- **Training sample size:** 6,779 SPY returns, 1993-02-01 through 2019-12-31. Reserved test sample: 1,684 returns, 2020-01-02 through 2026-09-15. Total usable SPY returns: 8,463.
- **Result:** 21 supporting tests passed. Preliminary fits converged without captured warnings. Parameter counts including means/distribution parameters: ARCH 3, GARCH 4, GARCH-t 5, GJR-GARCH-t 6. GJR alpha is at its zero bound. Parameters, diagnostics, and two preliminary figures are saved under results/; figures were copied to article/figures/.
- **Interpretation:** These are training fits, not evidence of out-of-sample downside predictability. Fitted paths use full-training parameter estimates and cannot serve as historically available ML features. The missing-data audit is relative to supplied SPY dates, not a full exchange calendar.
- **Notebook status:** The user requested a learning walkthrough before execution. No notebook code cells have been executed; the notebook has no outputs. Calculations, fits, and charts remain prompts to build together. Part 1 is not complete.
- **Next step:** Work through the notebook with the user, starting with data inspection and return calculations. Do not automatically execute or fill in the remaining exercises; do not start Part 2.

## 2026-09-18 — Part 1 article and first public repository preparation

- **Question:** What do the four fitted models teach us about squared shocks, persistence, tails, and asymmetry before testing downside forecasts?
- **Model / change:** Prepared a standalone Part 1 article and a seven-part series guide. Added canonical LaTeX equations, reproducible PNG equation rendering, a Medium upload copy, an HTML reading preview, and a model-table image. Updated setup/data instructions and publishing checklist. Kept raw inputs, AI conversations, local tools, and runtime files ignored.
- **Data used:** Existing checksum-verified snapshot; no fresh provider download. SPY has 8,464 price dates matching the XNYS reference sessions. VIX's 328 additional rows consist of 307 null-close non-session rows, 19 populated dates before SPY coverage, and two populated dates outside the equity calendar (2026-05-25 and 2026-09-07). Those extra dates require source investigation before any use; all SPY dates have VIX closes. Part 1 fits use SPY only.
- **Training sample size:** 6,779 returns through 2019-12-31; 1,684 later returns reserved from forecast evaluation.
- **Result:** 21 tests passed. Executed the supporting model script and complete notebook in an isolated temporary copy with a fresh kernel, preserving the working notebook. Four supporting CSV tables and three notebook CSV tables matched saved reference values using `rtol=1e-8`, `atol=1e-10`. The comparison tolerance is an engineering allowance for numerical differences, not a statistical significance threshold or cross-platform guarantee. Model fits reported convergence without captured fitting warnings. Notebook format and rendered equations were checked. Removed the local project path from a saved notebook output. No notebook code changed during article preparation.
- **Interpretation:** These are in-sample results and controlled response scenarios, not out-of-sample forecasts, causal explanations, or evidence of economic value. GJR alpha is at the zero boundary. Validation reused the preserved local snapshot and installed locked environment; it did not establish clean-checkout data availability or validate a fresh installation on another platform.
- **Publication status:** Prepared for the public `rwuebker/left-tail-volatility` repository. Medium text is a review draft, not a published Medium story. Frozen-data distribution and checks against immutable reference hashes remain unfinished and are disclosed in both README and article.
- **Next step:** Review the Part 1 article for Medium. Resolve exact-input distribution before claiming full fresh-checkout reproducibility. Continue with Part 2 only as a separate reviewed research step.

## 2026-09-18 — Add economic-value question to the series

- **Question:** Would reducing SPY exposure during predicted high downside risk improve out-of-sample investment outcomes after costs?
- **Change:** At the author's request, extend the original forecasting-only scope with a narrow SPY/cash experiment and a conclusion for every part. Added BACKTEST_PLAN.md with proposed heuristic defaults, delayed execution, baseline comparisons, accounting checks, and final-test reuse restrictions.
- **Result:** Planning and article changes only. No forecasts, strategy returns, or new empirical results were generated. First downside-driven implementation belongs in Part 2. Exact evaluation dates and refit schedules must be frozen before results are inspected.
- **Interpretation:** Forecast accuracy, economic value, and reduced exposure are different claims. The revised Part 1 conclusion makes their current limits explicit.

## 2026-09-18 — Execute the Part 1 allocation pilot

- **Authorization / scope:** The author explicitly requested adding the backtest to Notebook 01 and showing results, superseding the earlier plan to wait for Part 2.
- **Question:** Does the fixed GJR downside-risk allocation improve investment outcomes after costs?
- **Protocol before results:** Recorded `config/part1_backtest.json`: fit through 2019, no refits, 2020 threshold warmup, entry at first 2021 close, 100%/50% SPY based on the prior-252-forecast 80th percentile, 20,000 five-session Monte Carlo paths with date-keyed seeds, 20-session historical baseline, zero cash return, 0/5/10 basis point cost cases, next-close execution, terminal liquidation. No parameters were selected by searching strategy performance.
- **Data:** Original SPY snapshot verified against the committed SHA-256 manifest and the XNYS session calendar. No new downloads. Training: 6,779 returns. Entry 2021-01-04; first earned return 2021-01-05; final date 2026-09-15; 1,430 daily return intervals.
- **Result:** At 5 basis points, GJR CAGR 12.87%, maximum drawdown -19.66%, volatility 13.48%, average exposure 89.65%; buy-and-hold CAGR 14.94%, drawdown -24.50%; historical-risk rule CAGR 13.36%, drawdown -20.15%. Saved forecasts, thresholds, primary daily ledgers, cost-scenario metrics, annual returns, configuration hashes, versions, and chart in results/backtest/.
- **Validation:** 32 tests passed, including 11 new checks for causal forecasts, threshold exclusion of the present score, delayed execution, known downside moments, self-financing rebalancing after costs, market-drift turnover, cash/all-SPY cases, and compounding. New notebook supplement executed in a fresh kernel while preserving earlier code/outputs.
- **Interpretation:** Smaller drawdown and lower return; no demonstrated economic or statistical superiority. GJR has more turnover than the historical signal. Median Monte Carlo SE/forecast approximately 1.3%; it excludes parameter uncertainty. Zero cash interest, fixed costs, no taxes/market impact, and a single observed historical period limit conclusions. The 2020 crash is not evaluated. The 2021 and 2026 annual rows are partial years.
- **Next step:** Review the notebook results together before Part 2; do not tune to the now-observed evaluation period without labeling the work exploratory.

## 2026-09-18 — Expand the article’s backtest charts

- **Request:** Show more trading-strategy results as charts directly in the Part 1 article.
- **Change:** Added four reproducible charts: wealth/drawdown, annual returns, risk-threshold/exposure behavior, and cost sensitivity/turnover. Embedded them with captions and alt text in the article and regenerated the Medium and HTML copies.
- **Data / validation:** Used existing results/backtest CSVs only, without rerunning or tuning the experiment. The chart script checks terminal wealth, maximum drawdowns, and annual compounding against the saved daily ledger and metrics. Partial years/months and cost/cash assumptions are labeled.
- **Interpretation:** The figures show both reduced losses and forgone gains. No model-performance claim or backtest setting changed.
