CURRENT SCOPE UPDATE — 2026-09-18

The author requested a conclusion for each installment and a simple out-of-sample SPY/cash allocation experiment. Follow BACKTEST_PLAN.md for this narrow addition. It supersedes the original prohibition on all trading-strategy work; broader strategies and hedging remain deferred. Begin the downside-driven backtest in Part 2 after constructing valid forecasts, then apply the same protocol to subsequent models. Part 1's conclusion must state that economic value has not yet been tested.

The original guide follows for context.

Create a new quantitative research project in the current workbench directory:

left-tail-volatility

PROJECT TITLE

Predicting the Left Tail:
Can GARCH and Machine Learning Warn Us About Downside Risk?

PROJECT PHILOSOPHY

This project should prioritize:

1. understanding the models
2. realistic sample-size discussion
3. correct out-of-sample testing
4. tests for all important source-code calculations
5. reproducibility
6. clear writing
7. publishing the research as we go

Do not try to build every possible volatility model.

Do not design a trading strategy yet.

First determine whether downside risk is actually predictable.

The project should be understandable to a technically interested reader who is not already a volatility specialist.

Use plain descriptive language.

Whenever technical language is necessary, define it immediately.

==================================================
PRIMARY RESEARCH QUESTION

Can information available today predict unusually high downside volatility in the S&P 500 over the next five trading days?

Primary target:

future 5-day downside realized variance.

Define:

DSV(t,t+5) =
sum of future squared returns for days where the return is negative.

Mathematically:

DSV(t,t+5)

sum[r_i^2 * I(r_i < 0)]

for i from t+1 through t+5.

Plain English:

How much negative price movement occurs during the next five trading days?

Also calculate ordinary future realized variance so we can compare:

total volatility

versus

downside volatility.

==================================================
PROJECT STRUCTURE

Create:

left-tail-volatility/
README.md
PROJECT_PLAN.md
RESEARCH_LOG.md
pyproject.toml
Makefile
.gitignore

notebooks/
    01_garch_foundations.ipynb
    02_downside_target_and_forecasts.ipynb
    03_machine_learning.ipynb
    04_lstm.ipynb
    05_hybrid_models.ipynb
    06_model_comparison.ipynb
    07_final_results.ipynb
src/
    left_tail/
        __init__.py
        data.py
        targets.py
        garch.py
        features.py
        ml.py
        lstm.py
        validation.py
        metrics.py
        plots.py
tests/
    test_data.py
    test_targets.py
    test_features.py
    test_garch_helpers.py
    test_validation.py
    test_metrics.py
scripts/
    download_data.py
    run_garch.py
    run_ml.py
    run_lstm.py
    run_hybrid_models.py
    generate_results.py
results/
    figures/
    tables/
    forecasts/
article/
    medium_draft.md
    figures/
    medium_publish_checklist.md

==================================================
TESTING REQUIREMENT

All important reusable src/ code must have tests.

Prioritize tests that protect the validity of the research.

Required tests include:

1. daily-return calculation
2. downside-variance calculation
3. forward 5-day target construction
4. target uses t+1 through t+5 and never includes time t
5. features at time t contain no information from t+1 or later
6. chronological train/test splitting
7. feature scaling uses training data only
8. walk-forward predictions use historical information only
9. rolling calculations use past windows only
10. performance metrics produce expected values on simple known examples

Do not spend excessive time unit-testing visualization code.

Run pytest regularly.

No phase is complete while its tests are failing.

==================================================
MEDIUM ARTICLE — START IMMEDIATELY

Create:

article/medium_draft.md

Working title:

Predicting the Left Tail:
Can GARCH and Machine Learning Warn Us About Downside Risk?

Start writing the article during Part 1.

Do not wait for the experiment to finish.

The article should evolve with the research.

Use this provisional structure:

1. What are we trying to predict?
2. Why volatility is not always bad
3. Why downside volatility matters
4. ARCH in plain English
5. GARCH in plain English
6. Why +4% and -4% look identical to ordinary GARCH
7. GJR-GARCH and negative shocks
8. Fat tails and Student-t errors
9. How much data do these models actually need?
10. Building the downside-risk target
11. A conventional machine-learning model
12. Does adding the GARCH forecast help machine learning?
13. An LSTM and the small-data problem
14. Does adding the GARCH forecast help the LSTM?
15. Model comparison
16. What worked
17. What failed
18. What we would investigate next
19. Reproducing the results

Maintain this file continuously.

==================================================
MEDIUM PUBLISHING CHECKLIST

Create:

article/medium_publish_checklist.md

Include instructions for the final publishing process:

* create/open Medium draft
* copy cleaned article text section-by-section
* format title and subheaders
* use Medium code blocks for short code snippets
* use inline code for variable names
* upload exported PNG charts
* add chart captions
* add alt text
* link prominently to GitHub repository
* optionally embed a GitHub Gist for longer code examples
* render important equations as clear images if needed
* add appropriate Medium topics
* preview before publishing
* verify all links and figures after publication

Do not make the Medium article a code dump.

Keep code examples short.

GitHub should contain the full reproducible implementation.

==================================================
PART 1 — GARCH FOUNDATIONS
Approximate days 1-2

DATA

Use daily SPY data.

Also obtain:

VIX

and VIX3M if easily available.

Document:

* data source
* first date
* last date
* number of observations
* missing observations

MODELS

Teach and fit:

1. ARCH
2. GARCH(1,1)
3. GARCH(1,1) with Student-t errors
4. GJR-GARCH with Student-t errors

Do not add more GARCH variants yet.

EXPLANATION

Explain:

omega
alpha
beta
alpha + beta
gamma
Student-t degrees of freedom

Use plain language.

Explain why:

(+4%)^2 = (-4%)^2

causes standard GARCH to treat equal positive and negative shocks the same.

Demonstrate the estimated response of GARCH and GJR-GARCH after:

+1% versus -1%
+2% versus -2%
+4% versus -4%

Create a publication-quality figure.

SAMPLE SIZE

Report:

* total observations
* training observations
* test observations
* estimated parameter count

Explain why several thousand daily observations can be reasonable for a model with only a small number of estimated parameters.

Do not use universal rules such as:

“GARCH requires X observations.”

Explain sample size relative to model complexity.

OUTPUT

Create:

notebooks/01_garch_foundations.ipynb

Update Medium draft with Parts 1-8.

Run tests.

Update RESEARCH_LOG.md.

==================================================
PART 2 — DOWNSIDE FORECASTING TARGET
Approximate days 3-4

Build:

* daily realized variance
* daily downside variance
* forward 1-day downside variance
* forward 5-day downside variance
* forward 10-day downside variance

Primary target remains 5-day downside variance.

Create intuitive charts comparing:

total volatility

versus

downside volatility.

Implement true chronological / walk-forward evaluation.

Use GJR-GARCH-t as the main econometric model.

Determine how its conditional volatility forecast should be converted or related to the future downside-risk target.

Do not silently pretend a total-volatility forecast is identical to a downside-volatility forecast.

Document the exact relationship and limitations.

Create:

notebooks/02_downside_target_and_forecasts.ipynb

Add article sections explaining:

* how the target is defined
* why five days was selected initially
* what GARCH can and cannot forecast
* sample-size implications

==================================================
PART 3 — CONVENTIONAL MACHINE LEARNING
Approximate days 5-6

Use one main boosting model.

Preferred initial choice:

XGBoost.

Before implementing it, document why it was chosen over alternatives such as:

* random forest
* LightGBM
* CatBoost

Keep the discussion practical.

For example:

* nonlinear relationships
* interaction effects
* works well with modest tabular datasets
* strong regularization options
* does not require deep-learning-scale datasets

BASE ML EXPERIMENT

First run XGBoost WITHOUT any GARCH forecast as a feature.

Use only information directly observable at time t.

Possible features:

* 1-day return
* 5-day return
* 20-day return
* recent realized volatility
* recent downside volatility
* current drawdown
* number of negative-return days in recent window
* largest recent negative return
* VIX
* VIX3M or VIX term structure if available

Keep feature count modest.

Do not generate hundreds of technical indicators.

Use chronological validation.

No shuffled cross-validation.

Document:

* training sample size
* test size
* feature count
* important hyperparameters
* approximate model complexity
* tuning procedure

Keep tuning modest.

Create:

notebooks/03_machine_learning.ipynb

==================================================
PART 4 — SMALL LSTM
Approximate days 7-8

Create one deliberately small LSTM.

FIRST LSTM EXPERIMENT

Do NOT include the GARCH forecast initially.

Use only raw/history-derived inputs.

Possible sequence inputs:

* daily return
* recent downside variance
* VIX
* current drawdown

Use a sensible sequence length such as 20-60 trading days.

Determine a reasonable value experimentally but avoid excessive tuning.

Explicitly report:

* number of daily observations
* training observations
* sequence length
* resulting sequence count
* overlapping nature of sequences
* model parameter count
* training/validation/test dates
* training runtime

EXPLAIN SAMPLE SIZE CAREFULLY

If 4,000 overlapping sequences are produced, do NOT describe them as 4,000 independent market histories.

Explain that neighboring sequences contain much of the same information.

Discuss why this makes effective sample size smaller than raw sequence count.

The LSTM is an experiment, not a model expected to win.

Create:

notebooks/04_lstm.ipynb

Update Medium draft with:

* why use an LSTM?
* why might it fail?
* why deep learning generally benefits from richer datasets?
* why this experiment does not prove universal rules about neural networks

==================================================
PART 5 — HYBRID MODELS
Approximate days 9-10

This is an important experiment.

The order must be:

FIRST:
run ML and LSTM without GARCH-derived inputs.

THEN:
add the GJR-GARCH forecast as an additional input.

Experiment A:

XGBoost without GARCH forecast.

Experiment B:

XGBoost + GJR-GARCH forecast.

Experiment C:

LSTM without GARCH forecast.

Experiment D:

LSTM + GJR-GARCH forecast sequence/state.

For the LSTM, consider supplying the GJR-GARCH conditional volatility estimate at each historical point in the input sequence.

Example daily sequence vector:

[
return_t,
downside_variance_t,
VIX_t,
drawdown_t,
GJR_volatility_t
]

This allows the LSTM to observe how the econometric volatility estimate evolves through time.

Research question:

Does a traditional volatility model provide useful information to the machine-learning model beyond what the raw historical features already contain?

Do NOT interpret improvement as proof that the ML model “understands GARCH.”

It simply means the GARCH forecast may be a useful engineered feature.

Create:

notebooks/05_hybrid_models.ipynb

==================================================
PART 6 — MODEL COMPARISON AND SAMPLE-SIZE STUDY
Approximate days 11-12

Compare:

1. historical downside-volatility baseline
2. GJR-GARCH-t
3. XGBoost without GARCH
4. XGBoost with GARCH
5. LSTM without GARCH
6. LSTM with GARCH

Evaluate on the same out-of-sample dates whenever possible.

Metrics:

* MAE
* RMSE
* QLIKE if appropriate for the target
* correlation between prediction and realized downside volatility

Also create RISK BUCKETS.

For example:

sort predictions into five groups from lowest predicted downside risk to highest.

Then calculate actual subsequent downside volatility in each group.

This should answer:

When the model says risk is high, is actual future downside volatility meaningfully higher?

Create a sample-size/model-complexity table:

Model
Training observations
Test observations
Number of input features
Sequence length
Approximate parameter count
Forecast horizon
Retraining schedule
Runtime

Discuss:

raw sample size

versus

effective independent information.

Do not hide poor performance.

Create:

notebooks/06_model_comparison.ipynb

==================================================
PART 7 — FINAL FIRST DRAFT
Approximate days 13-14

Create:

notebooks/07_final_results.ipynb

README.md should become a concise research summary.

Finish the first complete Medium draft.

The first draft should answer:

1. What is volatility?
2. What is downside volatility?
3. What does GARCH actually forecast?
4. Why does asymmetry matter?
5. Why use Student-t errors?
6. How much data did we have?
7. Why was XGBoost appropriate?
8. Why was an LSTM questionable but still worth testing?
9. Did XGBoost beat the econometric model?
10. Did the LSTM beat simpler models?
11. Did adding the GARCH forecast improve XGBoost?
12. Did adding the GARCH forecast improve the LSTM?
13. Which model best separated low-risk and high-risk periods?
14. What failed?
15. What should we investigate next?

NEXT STEPS SHOULD BE DISCUSSION ONLY.

Possible next extensions:

* 5-minute intraday data
* realized volatility from intraday returns
* HAR-RV
* richer implied-volatility information
* historical SPY option skew
* cross-sectional stock universe
* trading / hedging implementation

Do not implement these unless the first draft is already complete and reviewed.

==================================================
REPRODUCIBILITY

The final first-draft experiment should run from scripts.

Target workflow:

uv sync
python scripts/download_data.py
pytest
python scripts/run_garch.py
python scripts/run_ml.py
python scripts/run_lstm.py
python scripts/run_hybrid_models.py
python scripts/generate_results.py

Core results must not require manually executing notebook cells.

Set random seeds.

Pin dependencies.

Save forecasts and result tables.

Record important experiment choices in RESEARCH_LOG.md.

==================================================
RESEARCH LOG

For each experiment record:

DATE
QUESTION
MODEL / CHANGE
DATA USED
TRAINING SAMPLE SIZE
RESULT
INTERPRETATION
NEXT STEP

This is especially important when comparing models.

==================================================
IMPORTANT GUARDRAILS

Do not add:

* intraday data during the first draft
* full option-chain data
* option-surface modeling
* trading strategies
* cross-sectional stocks
* HAR-RV
* transformers
* reinforcement learning
* huge hyperparameter searches

until the first complete draft has been produced.

Those are possible second-stage extensions.

==================================================
FIRST EXECUTION

Begin with Part 1 only.

1. Print current working directory.
2. Create ./left-tail-volatility.
3. Initialize Git.
4. Create the repository structure.
5. Create PROJECT_PLAN.md.
6. Create RESEARCH_LOG.md.
7. Create article/medium_draft.md.
8. Create article/medium_publish_checklist.md.
9. Create the Python environment using uv.
10. Download daily SPY, VIX, and VIX3M if readily available.
11. Report exact usable sample sizes.
12. Implement return and downside calculations.
13. Write tests.
14. Fit ARCH, GARCH, GARCH-t, and GJR-GARCH-t.
15. Create the positive-versus-negative shock comparison.
16. Create notebook 01_garch_foundations.ipynb.
17. Draft the first Medium sections.
18. Run pytest.
19. Execute notebook 01 completely.
20. Update RESEARCH_LOG.md.
21. Make logical Git commits.
22. STOP.

At the end report:

* files created
* tests passing/failing
* exact sample size
* GARCH parameter estimates
* any model-fitting warnings
* charts generated
* Medium sections drafted
* files I should review next

Do not continue to Part 2 until I review Part 1.