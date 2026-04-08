# Problem Statement
## Value at Risk Analysis on a Diversified US Equity Portfolio

---

### Academic Context

In financial risk management, the ability to quantify and communicate portfolio risk is a fundamental professional skill. Among the tools available to risk managers, **Value at Risk (VaR)** has become a standard benchmark, adopted by financial institutions, regulators, and portfolio managers worldwide since its popularization by J.P. Morgan in the 1990s.

---

### Research Question

**How can Value at Risk be estimated on a diversified US equity portfolio, and what are the differences between the Historical, Parametric, and Monte Carlo simulation methods at a 95% confidence level?**

---

### Objective

This project aims to apply and compare three methodologies for computing 1-day Value at Risk on a manually constructed, equally weighted US equity portfolio composed of five stocks from distinct economic sectors.

By computing VaR using three distinct approaches — historical simulation, parametric estimation, and Monte Carlo simulation — this study seeks to highlight the practical and theoretical differences between these methods, and to assess the implications of their underlying assumptions for risk estimation.

---

### Portfolio and Parameters

The portfolio consists of five US-listed equities selected for their sectoral diversity and market prominence:

- **LVMUY** (LVMH) — Luxury goods
- **JNJ** (Johnson & Johnson) — Healthcare
- **LMT** (Lockheed Martin) — Defense
- **NEE** (NextEra Energy) — Renewable energy
- **AAPL** (Apple) — Technology

Each stock is assigned an equal weight of 20%, ensuring simplicity and transparency in the portfolio construction. Daily price data is sourced from Yahoo Finance for the period January 2020 to December 2024, yielding approximately 1,250 observations.

The VaR parameters are fixed as follows:
- **Horizon:** 1 trading day
- **Confidence level:** 95%

---

### Methodology

Three standard risk estimation methods are applied:

1. **Historical Simulation:** The empirical distribution of past daily returns is used directly. The 5th percentile of this distribution provides the VaR estimate without any distributional assumption.

2. **Parametric Method (Variance-Covariance):** Returns are assumed to follow a normal distribution. VaR is computed analytically using the mean and standard deviation of historical returns, combined with the 5th percentile z-score of the standard normal distribution (z = −1.645).

3. **Monte Carlo Simulation:** A large number of random return scenarios (10,000) are generated from a normal distribution calibrated on historical data. The 5th percentile of the simulated outcomes serves as the VaR estimate.

---

### Expected Contributions

This project contributes to the understanding of market risk measurement at an introductory academic level. By comparing three methods on the same portfolio, it illustrates the sensitivity of VaR estimates to methodological choices, and provides a practical basis for discussing the assumptions, advantages, and limitations of each approach.

The results are supported by clear visualizations designed to facilitate interpretation and oral communication.

---

### Limitations

This study acknowledges several limitations. The assumption of normally distributed returns, embedded in the Parametric and Monte Carlo methods, is known to underestimate extreme losses due to the fat-tailed nature of financial return distributions. Furthermore, all three methods rely on historical data, implicitly assuming that past market conditions are representative of future risk. Finally, the equal-weighting scheme and the restricted universe of five stocks limit the representativeness of the portfolio relative to a real-world investment mandate.

---

*Master 1 Finance — IAE Metz — Academic Year 2025-2026*
