# Predicting the Left Tail

Can GARCH and Machine Learning Warn Us About Downside Risk?

Can information available today predict unusually high downside volatility in the S&P 500 over the next five trading days? We will use daily SPY returns and define the primary target as the sum of squared negative returns on days t+1 through t+5.

## Current status

Part 1 has been worked through: data checks, return calculations, four model fits, and controlled shock-response comparisons. The notebook includes saved outputs. These are training-sample results, not out-of-sample forecast or economic-value evidence. Parts 2–7 are not implemented.

Read [Part 1: What does GARCH actually learn about volatility?](article/01_garch_foundations.md), browse the [seven-part article guide](article/SERIES.md), or open the [notebook](notebooks/01_garch_foundations.ipynb).

The repository contains code, reference estimates, and data-source checksums. Raw downloads are excluded. Exact-input reproduction from a fresh checkout remains pending the frozen-data distribution workflow described below.

## Environment

The reference environment uses **Python 3.11.14** on Apple Silicon. `.python-version` selects this project's version; `uv.lock` pins dependencies. Later machine-learning dependencies will be added in their corresponding phases.

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

`make test` runs the supporting calculation tests. Opening the notebook does not run its cells. Select `.venv/bin/python` as its kernel and work through one section at a time.

## Prepare the data and run Part 1

These instructions cover the current Part 1 workflow; the full seven-part experiment is not implemented yet. After obtaining the repository, open a terminal in its root directory (the directory containing `pyproject.toml`). Complete the environment setup above first. Internet access is required for dependency installation and the initial data download. The research does not require Codex authentication.

With the project environment activated:

```sh
# Download inputs, or verify and reuse the existing local snapshot.
python scripts/download_data.py

# Check the research calculations.
python -m pytest

# Open the notebook and work through its cells in order.
python -m jupyterlab notebooks/01_garch_foundations.ipynb
```

The downloader requests dates from **1993-01-01 through 2026-09-15**, using an exclusive end date of 2026-09-16. It writes `SPY_source.csv`, `VIX_source.csv`, available VIX3M inputs, `daily_prices.csv`, and `manifest.json` under `data/raw/`. These files are ignored by Git and are absent from a fresh checkout. The notebook reads those files; it does not download them. If you see `FileNotFoundError` when loading SPY, run the download command from the repository root first.

VIX3M is optional in the downloader, but the notebook's VIX/VIX3M audit requires both files. If VIX3M is unavailable, inspect `optional_failures` in the manifest and resolve the source failure before running that audit; do not substitute fabricated values.

To regenerate the preliminary GARCH tables and figures without manually executing notebook cells, run:

```sh
python scripts/run_garch.py
```

This fits the Part 1 models and writes supporting results under `results/` and `article/figures/`. It is optional during the guided walkthrough and can overwrite existing generated results. Saved notebook outputs are not evidence that your current kernel has executed the cells.

### Current reproducibility limitation

The downloader verifies an existing snapshot against its **local** manifest. On a fresh download, it creates new checksums; it does **not** check them against the original research snapshot. It also writes `results/tables/data_manifest.json`, replacing the working copy of the reference manifest. Preserve the reference from the published Git revision when comparing snapshots.

Historical provider data, including adjusted prices, can change even for the same requested dates. Consequently, these commands reproduce the procedure but do not yet guarantee the original inputs or identical estimates. Before publication, we must provide a permitted frozen snapshot, verify it against reference checksums, and test a clean-checkout run against reference results with documented numerical tolerances. That distribution and verification workflow is not implemented yet.

An existing snapshot is reused by default. Only for an intentional new data experiment, use `python scripts/download_data.py --refresh`; this replaces the local snapshot and its manifests. Do not use it to reproduce the original sample.

## Guide

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete supplied brief and [RESEARCH_LOG.md](RESEARCH_LOG.md) for decisions. The seven phases are approximate two-day milestones. **Stop after Part 1 for review before beginning Part 2.**

The repository contains directories for source code, tests, scripts, notebooks, data, results, and the evolving article. Experiment scripts and notebooks will be created as they are implemented; empty directories are placeholders, not finished outputs.

## Part 1 supporting files

- `scripts/download_data.py`: download SPY/VIX from Yahoo Finance and VIX3M from Cboe when Yahoo history is insufficient. Reuses a checksummed local snapshot; `--refresh` explicitly replaces it.
- `scripts/run_garch.py`: optional full supporting run, already used for preliminary fits. It is **not called by the guided notebook**.
- `results/tables/data_manifest.json`: source and coverage audit; raw snapshots are ignored by Git.
- `results/tables/part1_summary.json`: preliminary fit sample sizes and optimizer diagnostics.

The reference snapshot contains 8,463 SPY returns, with 6,779 through 2019 for fitting and 1,684 later observations reserved. VIX3M begins on 2009-09-18. The notebook additionally checks SPY dates against the XNYS exchange calendar: all 8,464 expected sessions are present. For VIX and VIX3M, that equity calendar is an alignment reference, not proof of the indexes’ historical publication schedules. The archived raw inputs are required to reproduce identical estimates; later vendor downloads can be revised.

Part 1 is prepared for article review. The subsequent research phases remain separate work.

## Open the guided notebook

JupyterLab is included in the locked development dependencies. From the repository root, after activating `.venv`, run:

```sh
python -m jupyterlab notebooks/01_garch_foundations.ipynb
```

Opening the notebook starts its kernel but does not execute cells. Work through them individually.

## Codex beside the notebook

Jupyter AI is installed in the locked development environment. Its Codex adapter is installed locally under `.tools/codex-adapter`. To recreate it:

```sh
npm install --prefix .tools/codex-adapter --save-exact @agentclientprotocol/codex-acp@1.12.0
codex login status
sh scripts/start_notebook.sh
```

The launcher exposes the adapter on PATH and starts token-protected JupyterLab on localhost port 8889. Open the token URL printed by Jupyter, then open the notebook and the Jupyter Chat sidebar. Create a chat and select Codex. Attach cells or files with the attachment button. Project tutoring instructions are in AGENTS.md. Existing Codex authentication is reused; a separate login may be required on another machine.

Saved outputs do not initialize a fresh kernel: run the cells in order to recreate variables. Use one editing session per notebook to avoid competing saves. The optional AI integration is not required to reproduce the research.

## Article publishing assets

The canonical article uses LaTeX display equations. To regenerate the Medium version, equation PNGs, and the local HTML reading preview:

```sh
python scripts/render_article.py
```

Open `article/01_garch_foundations.html` locally, or use the Markdown version on GitHub. See [the Medium publishing checklist](article/medium_publish_checklist.md). No Medium article has been published yet.
