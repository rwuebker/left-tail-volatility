# Predicting the Left Tail:
## Can GARCH and Machine Learning Warn Us About Downside Risk?

*Working draft. Experiments are still to come.*

### 1. What are we trying to predict?

I've been wondering how much a volatility forecast tells us about the downside. A 4% rally and a 4% drop contribute equally to a squared-return measure, but I'd be more concerned about one of them if I were holding the market.

Could we forecast just the negative movement?

We'll explore that using SPY, an exchange-traded fund that tracks the S&P 500. We'll start with the next five trading days—roughly a week—and see whether today's information helps explain how much prices fall during that window.

### 2. Why volatility is not always bad

Volatility describes how widely returns vary. It includes movement in both directions.

For this project, we'll measure total movement by adding up squared daily returns. Squaring makes larger moves count more, and gives equal weight to a rise or fall of the same size.

I'm curious whether separating the negative days makes the result any easier to predict.

### 3. Why downside volatility matters

Our downside measure keeps only those negative days: square each negative return and add the values over the next five trading days. Positive days contribute zero.

That's **downside realized variance**. “Realized” means measured from returns that actually occurred. Variance is in squared-return units; its square root gives a volatility measure.

A rebound won't cancel an earlier decline in this calculation, so it measures something different from the week's net loss. Small declines count too; we're not limiting it to crashes.

We'll use information through today to predict this quantity from tomorrow onward. Do weeks with higher predictions end up having more negative movement?

### 4. ARCH in plain English

We'll begin with ARCH, which estimates variance using recent squared shocks. A shock is the difference between the return observed and the return the model expected.

In this model, a bigger surprise can raise the estimate of what comes next. The size of that response is something we'll fit from the data.

### 5. GARCH in plain English

GARCH also uses the previous variance estimate, letting the effect of older shocks carry forward.

GARCH(1,1) has three main variance coefficients: **omega**, a baseline term; **alpha**, the weight on the latest squared shock; and **beta**, the weight on the previous variance estimate. Under the standard assumptions, alpha plus beta describes persistence. Closer to one means a shock's effect fades more slowly. [Model equations](https://arch.readthedocs.io/en/latest/univariate/generated/arch.univariate.GARCH.html).

That gives us a way to estimate how long a surprise continues to matter.

### 6. Why +4% and -4% look identical to ordinary GARCH

There is a detail here that brings us back to the original question:

**(+4%)² = (−4%)²**

Ordinary GARCH responds equally to positive and negative shocks of the same size. Here, shocks are measured relative to the expected return; they match raw returns when that expectation is zero.

Would allowing different responses help with the downside forecast?

### 7. GJR-GARCH and negative shocks

GJR-GARCH adds **gamma**, a coefficient that gives negative squared shocks an extra effect. Its estimated value tells us how that response differs.

We'll compare the fitted models after positive and negative shocks of 1%, 2%, and 4%. Seeing those responses side by side should help make the coefficients less abstract.

### 8. Fat tails and Student-t errors

Another choice is how much room the model allows for extreme surprises. We'll compare normal errors with Student-t errors, which have heavier tails. The Student-t **degrees of freedom** control the tail weight: smaller values mean heavier tails. [ARCH and Student-t examples](https://bashtage.github.io/arch/univariate/univariate_volatility_modeling.html).

We'll see how much that changes the estimates and, later, the forecasts on unseen dates.

There's also a connection we haven't worked out yet. These models forecast conditional variance—variance given the available information—while our target counts only negative returns. How should we get from one to the other? That's one of the next questions in the experiment.

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

