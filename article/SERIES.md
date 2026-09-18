# Predicting the Left Tail

Can GARCH and machine learning warn us about downside risk?

Seven articles accompany seven notebooks. Only Part 1 is drafted; later titles describe planned experiments, not established results. Medium URLs will be added after publication.

1. [What does GARCH actually learn about volatility?](01_garch_foundations.md) — [Notebook 01](../notebooks/01_garch_foundations.ipynb).
2. Defining and forecasting downside risk — planned.
3. Can machine learning improve the forecast? — planned.
4. Can an LSTM learn from this much data? — planned.
5. Does adding GARCH information help? — planned.
6. Which forecasts hold up on unseen data? — planned.
7. What did we learn about predicting the left tail? — planned.

Each published installment will link to this guide, its notebook, and its available previous/next installments. Articles are drafted from reviewed experiments; future performance is not assumed.

## Article formats

- `01_garch_foundations.md`: canonical article, with LaTeX display equations for GitHub.
- `01_garch_foundations_medium.md`: generated copy with PNG equations for uploading to Medium.
- `01_garch_foundations.html`: generated local reading preview with equations, code, and figures.
- `equations/`: equation images for the Medium version.

After editing the canonical article, regenerate the publishing assets from the repository root:

```sh
python scripts/render_article.py
```

See [the publishing checklist](medium_publish_checklist.md) for the final manual Medium steps.
