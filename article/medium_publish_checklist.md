# Medium publishing checklist — Part 1

## Prepare

- [ ] Review `01_garch_foundations.md` for voice, mathematical notation, and empirical claims.
- [ ] Run `python scripts/render_article.py` from the repository root after changing the article.
- [ ] Review `01_garch_foundations.html` locally; check equations and charts at mobile width.
- [ ] Confirm the GitHub repository and notebook links resolve at the intended revision.
- [ ] Keep the current frozen-data limitation visible; do not promise identical fresh-download results.

## Transfer to Medium

- [ ] Create a Medium draft titled **How GARCH Models Volatility: Shocks, Persistence, and Asymmetry** with subtitle **Predicting the Left Tail · Part 1 of 7**.
- [ ] Copy the text from `01_garch_foundations_medium.md` section by section. This is an upload guide, not a guarantee of automatic Markdown import.
- [ ] Format headings and short code snippets using Medium's editor. Preserve indentation and plain-text code, including `fill_method=None` and the training cutoff.
- [ ] Upload `equations/part1_01.png` through `equations/part1_15.png` at their matching image markers. The canonical Markdown retains the editable LaTeX. Use the surrounding explanation and equation alt text to provide an accessible text equivalent.
- [ ] Upload the four backtest charts at their image markers: `figures/backtest_growth_drawdown.png`, `figures/backtest_annual_returns.png`, `figures/backtest_exposure.png`, and `figures/backtest_cost_sensitivity.png`. Preserve captions, partial-year labels, cost assumptions, and alt text.
- [ ] Upload `figures/shock_responses.png` and `figures/training_volatility.png`; retain their captions and descriptive alt text.
- [ ] Upload `figures/part1_model_comparison.png` at the model-table marker. The canonical GitHub article retains the values in an accessible text table; keep that link and the AIC explanation.
- [ ] Use absolute GitHub links for the repository, README instructions, and notebook. Replace relative links when copying from the GitHub source.
- [ ] Add a series-guide link. Part 1 has no previous installment; label Part 2 as in preparation until it has a published URL. Add Next/Previous links as later articles are published.
- [ ] Add the installment to a public Medium List for the series.

## Final review

- [ ] Preview on desktop and mobile, including mathematical minus signs, subscripts, code, captions, and links.
- [ ] Confirm that in-sample fits are not described as out-of-sample forecasts or evidence of profitability.
- [ ] Publish only after author review; record the Medium URL in `SERIES.md` and the repository README.
- [ ] Verify the published article's links and images.

Medium formatting reference: https://help.medium.com/hc/en-us/articles/215194537-Using-the-story-editor
