# Predicting the Left Tail

Can GARCH and Machine Learning Warn Us About Downside Risk?

Can information available today predict unusually high downside volatility in the S&P 500 over the next five trading days? We will use daily SPY returns and define the primary target as the sum of squared negative returns on days t+1 through t+5.

## Current status

Part 1 setup: repository and isolated Python environment. No data downloaded, models fitted, or empirical findings produced yet.

## Environment

Python **3.11.14**, using the existing native Apple Silicon interpreter at `/opt/homebrew/bin/python3.11`. The shell default is a separate Python 3.14 installation. `.python-version` selects this project's version; `uv.lock` pins dependencies. Later machine-learning dependencies will be added in their corresponding phases.

A project-local installation of uv is in `.tools`; it and `.venv` are excluded from Git. Run from this directory:

```sh
# On a fresh checkout, bootstrap uv with an installed Python 3.11:
python3.11 -m venv .tools
.tools/bin/python -m pip install uv==0.12.15

# Recreate the locked research environment:
make sync
source .venv/bin/activate
python --version
```

Alternatively, with uv installed globally, run `uv sync --locked`. To use the local copy directly: `UV_CACHE_DIR=.uv-cache .tools/bin/uv run --locked python ...`.

`make test` will run the research tests when calculations are implemented. There are no calculation tests yet; an empty test suite is not a passing research milestone.

## Guide

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete supplied brief and [RESEARCH_LOG.md](RESEARCH_LOG.md) for decisions. The seven phases are approximate two-day milestones. **Stop after Part 1 for review before beginning Part 2.**

The repository contains directories for source code, tests, scripts, notebooks, data, results, and the evolving article. Experiment scripts and notebooks will be created as they are implemented; empty directories are placeholders, not finished outputs.
