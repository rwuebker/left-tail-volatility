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
