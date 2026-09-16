# Predicting the Left Tail

Can GARCH and Machine Learning Warn Us About Downside Risk?

Can information available today predict unusually high downside volatility in the S&P 500 over the next five trading days? We will use daily SPY returns and define the primary target as the sum of squared negative returns on days t+1 through t+5.

## Current status

Part 1 guided notebook created at `notebooks/01_garch_foundations.ipynb`. Its code cells are unexecuted and its calculations/fits are prompts to work through together. A data snapshot and preliminary supporting script outputs are available; these are not a completed or reviewed Part 1 notebook.

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

`make test` runs the supporting calculation tests (21 passing at creation). The notebook remains unexecuted by design. Select `.venv/bin/python` as its kernel and work through one section at a time.

## Guide

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete supplied brief and [RESEARCH_LOG.md](RESEARCH_LOG.md) for decisions. The seven phases are approximate two-day milestones. **Stop after Part 1 for review before beginning Part 2.**

The repository contains directories for source code, tests, scripts, notebooks, data, results, and the evolving article. Experiment scripts and notebooks will be created as they are implemented; empty directories are placeholders, not finished outputs.

## Part 1 supporting files

- `scripts/download_data.py`: download SPY/VIX from Yahoo Finance and VIX3M from Cboe when Yahoo history is insufficient. Reuses a checksummed local snapshot; `--refresh` explicitly replaces it.
- `scripts/run_garch.py`: optional full supporting run, already used for preliminary fits. It is **not called by the guided notebook**.
- `results/tables/data_manifest.json`: source and coverage audit; raw snapshots are ignored by Git.
- `results/tables/part1_summary.json`: preliminary fit sample sizes and optimizer diagnostics.

The initial snapshot contains 8,463 SPY returns, with 6,779 through 2019 for fitting and 1,684 later observations reserved. VIX3M begins on 2009-09-18. Missingness is checked against supplied source rows and observed SPY dates, not an independent exchange-session calendar. The archived raw inputs are required to reproduce identical estimates; later vendor downloads can be revised.

Part 1 remains open until we have worked through and reviewed the notebook together.
