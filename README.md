# Value at Risk (VaR) Analysis — US Equity Portfolio
### Master 1 Finance — IAE Metz — Group Project

---

## Project Objective

This project measures the **daily market risk** of a diversified US equity portfolio using **Value at Risk (VaR)** — one of the most widely used risk metrics in the financial industry.

We compare three standard methods to estimate VaR:
- **Historical VaR** — based purely on past returns
- **Parametric VaR** — based on the assumption that returns are normally distributed
- **Monte Carlo VaR** — based on random simulation of future returns

The goal is to understand how different methods produce different risk estimates, and what those differences mean in practice.

---

## Portfolio Composition

| Ticker | Company | Sector |
|--------|---------|--------|
| LVMUY | LVMH | Luxury |
| JNJ | Johnson & Johnson | Healthcare |
| LMT | Lockheed Martin | Defense |
| NEE | NextEra Energy | Renewable Energy |
| AAPL | Apple | Technology |

**Weighting:** Equal weight — 20% per stock.
**VaR horizon:** 1 day
**Confidence level:** 95%
**Analysis period:** January 2020 — December 2024

---

## Data Source

All data is downloaded automatically from **Yahoo Finance** using the `yfinance` Python library.
No manual file download is required.

We use the **Adjusted Close** price, which accounts for dividends and stock splits.

---

## Project Structure

```
Cours_SGBD_PYTHON_Master1_IAE_METZ/
│
├── DATA/                          <- Generated automatically by the scripts
│   ├── LVMUY.csv, JNJ.csv, ...   <- Raw price data per stock
│   ├── prices_clean.csv           <- Clean combined price table
│   ├── returns.csv                <- Daily returns per stock
│   ├── portfolio_returns.csv      <- Daily portfolio returns
│   ├── portfolio_value.csv        <- Simulated portfolio value
│   ├── var_results.csv            <- VaR results (all 3 methods)
│   ├── mc_simulations.csv         <- Monte Carlo simulation data
│   └── chart1 to chart4 (.png)   <- All visualizations
│
├── SCRIPTS/                       <- Python scripts (run in order)
│   ├── 01_download_data.py        <- Download data from Yahoo Finance
│   ├── 02_clean_data.py           <- Inspect and clean data
│   ├── 03_compute_returns.py      <- Calculate daily returns
│   ├── 04_portfolio.py            <- Build equal-weight portfolio
│   ├── 05_var_calculations.py     <- Compute Historical, Parametric, Monte Carlo VaR
│   ├── 06_visualizations.py       <- Generate all charts
│   └── main.py                    <- Run the full pipeline at once
│
└── PRESENTATION/                  <- Slides and oral presentation materials
```

---

## Installation

Make sure Python 3.8+ is installed. Then install the required libraries:

```bash
pip install yfinance pandas numpy matplotlib scipy
```

---

## How to Run the Project

### Option 1 — Run everything at once (recommended)
```bash
cd SCRIPTS
python main.py
```

### Option 2 — Run scripts one by one (step by step)
```bash
cd SCRIPTS
python 01_download_data.py
python 02_clean_data.py
python 03_compute_returns.py
python 04_portfolio.py
python 05_var_calculations.py
python 06_visualizations.py
```

All output files (data and charts) will appear in the `DATA/` folder.

---

## Methods Description

### Historical VaR
Uses the actual distribution of past returns. The 5th percentile of all historical daily returns is taken as the VaR estimate. No statistical assumption is made.

### Parametric VaR (Variance-Covariance)
Assumes that returns follow a Normal distribution. VaR is calculated analytically using the mean and standard deviation of historical returns, combined with a z-score of -1.645 (corresponding to the 5th percentile of a normal distribution).

### Monte Carlo VaR
Simulates 10,000 random return scenarios based on the historical mean and standard deviation. The 5th percentile of these simulations is the Monte Carlo VaR estimate.

---

## Interpreting the Results

| Method | Key Assumption | Main Advantage | Main Limitation |
|--------|---------------|----------------|-----------------|
| Historical | None | Captures real market events | Limited to past data |
| Parametric | Normal distribution | Simple and fast | Ignores fat tails |
| Monte Carlo | Normal simulation | Flexible | Depends on distribution choice |

---

## Limitations of the Project

- The analysis assumes **equal weighting**, which may not reflect a real portfolio strategy.
- All three methods assume that the **future will resemble the past** in some way.
- The **Parametric method** assumes normal returns, which underestimates extreme losses (fat tails).
- VaR does **not** tell you how large the loss will be when it exceeds the threshold — this is what CVaR (Conditional VaR) addresses, but it is beyond the scope of this project.
- The data period (2020–2024) includes the **COVID-19 crisis**, which may inflate the estimated risk.

---

## Requirements

```
Python >= 3.8
yfinance
pandas
numpy
matplotlib
scipy
```



---

## Contributor

- [Bochra Jabr](https://www.linkedin.com/in/bochra-jabr-a9a884245/)
