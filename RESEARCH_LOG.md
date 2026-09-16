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
