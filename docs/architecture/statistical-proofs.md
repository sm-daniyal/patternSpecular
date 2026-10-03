# Mathematical Derivations: Fisher's Exact Test for Longitudinal Bias Patterns

Pattern Specular rejects simple frequency counting in favor of exact statistical hypothesis testing. A managerial tendency is surfaced on the Pattern Dashboard if and only if it clears Fisher's exact test at $\alpha = 0.05$.

## 1. 2x2 Contingency Matrix

For a given bias category $C$ (e.g. gender-coded terminology) and demographic groups $G_1$ (e.g. female candidates) versus $G_2$ (e.g. male candidates), we construct the contingency table:

| Demographic | Language Flagged ($C$) | Language Not Flagged ($\neg C$) | Marginal Total |
|---|:---:|:---:|:---:|
| Group 1 ($G_1$) | $a$ | $b$ | $a + b$ |
| Group 2 ($G_2$) | $c$ | $d$ | $c + d$ |
| **Total** | $a + c$ | $b + d$ | $n = a + b + c + d$ |

## 2. Hypergeometric Probability Density Function

Under the null hypothesis $H_0$ that language usage is independent of candidate demographic attributes, the probability of observing matrix cell values with fixed row and column marginals is hypergeometric:

$$P(X = a) = \frac{\binom{a + b}{a} \binom{c + d}{c}}{\binom{n}{a + c}} = \frac{(a + b)!(c + d)!(a + c)!(b + d)!}{a! b! c! d! n!}$$

## 3. Two-Tailed Significance Computation

The two-tailed $p$-value aggregates the probabilities of all contingency tables $T$ that are as extreme or more extreme than the observed table $T_{obs}$:

$$p = \sum_{P(T) \le P(T_{obs})} P(T)$$

Surfacing rule:
$$\text{Surfaced} = 
\begin{cases} 
\text{True}, & \text{if } p < 0.05 \text{ and } (a + b + c + d) \ge 10 \\ 
\text{False}, & \text{otherwise} 
\end{cases}$$
