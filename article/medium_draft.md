# Predicting the Left Tail:
## Can GARCH and Machine Learning Warn Us About Downside Risk?

*An evolving research notebook in article form. We are starting the investigation; the results are still ahead of us.*

### 1. What are we trying to predict?

A market rises 4% in a day. Another day, it falls 4%.

Both are big moves. If we own the market, they feel very different.

That difference is where this project begins. When we say the market is becoming more volatile, what are we actually learning about the possibility of losses?

And can we learn anything useful before those losses arrive?

We will study SPY, an exchange-traded fund that tracks the S&P 500. Our question is deliberately narrow: **can information available today help predict the size of negative price movements over the next five trading days?**

Five days gives us a concrete place to start: roughly one trading week. Whether that is a useful horizon is itself something to investigate.

### 2. Why volatility is not always bad

Volatility describes how widely returns vary. It does not, by itself, tell us their direction.

One way to measure movement over a period is to square each daily return and add the results. Positive and negative moves both contribute. A large rally can therefore add just as much as a large decline.

For someone holding the market, that raises a question: how much of the movement in this measure is the kind we are worried about?

### 3. Why downside volatility matters

We will build a second measure that keeps only the negative days. Take each negative daily return, square it, and add those values over the next five trading days. Positive days contribute zero.

This is our **downside realized variance**. “Realized” means we calculate it from what actually happened. Variance uses squared-return units; taking its square root gives a volatility measure.

The target starts tomorrow. Today's return can help make the prediction, but it cannot be part of the future outcome we claim to predict.

This measure is not the week's total loss. A recovery does not cancel an earlier decline inside it. Nor is it a crash probability: even small negative days count. We are asking about the size of negative movements first.

Would weeks that look risky beforehand actually contain more of that movement?

### 4. ARCH in plain English

A natural starting question is whether recent surprises help predict the size of the next one.

ARCH estimates variance from past squared shocks. A shock is the difference between an observed return and the model's expected return. Bigger recent surprises can raise its estimate of future variance.

How much history should matter?

### 5. GARCH in plain English

GARCH adds the previous variance estimate to that calculation. It carries a memory of risk forward.

In GARCH(1,1), **omega** supplies a baseline term, **alpha** weights the latest squared shock, and **beta** weights the previous variance estimate. Under the standard model assumptions, alpha plus beta describes persistence: values closer to one imply slower fading of a shock's effect. [Model equations](https://arch.readthedocs.io/en/latest/univariate/generated/arch.univariate.GARCH.html).

But does the sign of that shock matter?

### 6. Why +4% and -4% look identical to ordinary GARCH

Squaring removes the sign:

**(+4%)² = (−4%)²**

Ordinary GARCH gives equal positive and negative shocks the same direct effect on variance. These are shocks relative to the expected return; they equal raw returns if that expectation is zero.

Is that symmetry useful here, or does it discard something we need?

### 7. GJR-GARCH and negative shocks

GJR-GARCH adds **gamma**, an extra coefficient applied to negative squared shocks. We will estimate it rather than assume negative surprises have a larger effect.

Our first comparison will ask how the fitted models respond to equal positive and negative shocks of 1%, 2%, and 4%.

### 8. Fat tails and Student-t errors

We will also compare normal errors with Student-t errors, which allow heavier tails: more room for extreme surprises. The estimated **degrees of freedom** control that tail weight; smaller values mean heavier tails. [ARCH and Student-t examples](https://bashtage.github.io/arch/univariate/univariate_volatility_modeling.html).

Will these changes improve predictions on dates the models have not seen? A better description of the past is only the beginning.

And we still have a gap to cross: these models forecast conditional variance—variance given the available information. Our target counts only future negative returns. We will need to explain that connection before comparing their forecasts.

That is our starting point. Before adding machine learning, we want to understand what the simpler models remember, what they ignore, and what evidence would persuade us that they can help.

### 9. How much data do these models actually need?

To be developed during the corresponding research phase.

### 10. Building the downside-risk target

To be developed during the corresponding research phase.

### 11. A conventional machine-learning model

To be developed during the corresponding research phase.

### 12. Does adding the GARCH forecast help machine learning?

To be developed during the corresponding research phase.

### 13. An LSTM and the small-data problem

To be developed during the corresponding research phase.

### 14. Does adding the GARCH forecast help the LSTM?

To be developed during the corresponding research phase.

### 15. Model comparison

To be developed during the corresponding research phase.

### 16. What worked

To be developed during the corresponding research phase.

### 17. What failed

To be developed during the corresponding research phase.

### 18. What we would investigate next

To be developed during the corresponding research phase.

### 19. Reproducing the results

To be developed during the corresponding research phase.

