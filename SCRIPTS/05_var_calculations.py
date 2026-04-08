# =============================================================================
# SCRIPT 05 - VALUE AT RISK (VaR) CALCULATIONS
# =============================================================================
# PURPOSE:
#   This script is the heart of the project. It computes Value at Risk (VaR)
#   using three different methods and compares the results.
#
# WHAT IS VALUE AT RISK (VaR)?
#   VaR answers this question:
#   "What is the maximum loss I can expect on a typical bad day?"
#
#   More precisely:
#   At a 95% confidence level, 1-day VaR = X means:
#   "There is a 95% chance that the portfolio will NOT lose more than X in one day."
#   (Equivalently: on the worst 5% of days, losses will exceed X.)
#
#   Example: if VaR = 1.5%, then on 95% of days, your daily loss will be < 1.5%.
#
# THE THREE METHODS:
#
#   1. HISTORICAL VaR
#      - Take all past daily returns (e.g., last 1250 days)
#      - Sort them from worst to best
#      - The 5th percentile is the Historical VaR
#      - Simple, no assumptions, but depends entirely on past data
#
#   2. PARAMETRIC VaR (also called Variance-Covariance method)
#      - Assume returns follow a Normal distribution
#      - Use the mean and standard deviation of past returns
#      - Apply a formula: VaR = -(mean - 1.645 * std)
#      - Fast and clean, but assumes normality (which is not always realistic)
#
#   3. MONTE CARLO VaR
#      - Simulate thousands of possible future return scenarios randomly
#      - Based on the same mean and std as the parametric method
#      - Take the 5th percentile of all simulated outcomes
#      - More flexible, shows the range of possible outcomes
#
# CONFIDENCE LEVEL: 95% -> We are looking for the 5th percentile of losses.
# VaR HORIZON: 1 day
# =============================================================================

# --- Import libraries ---
import pandas as pd     # For data manipulation
import numpy as np      # For numerical computations and random simulations
from scipy import stats # For the normal distribution (parametric method)
import os               # For file paths

# --- Define paths ---
DATA_FOLDER    = os.path.join(os.path.dirname(__file__), "..", "DATA")
INPUT_FILE     = os.path.join(DATA_FOLDER, "portfolio_returns.csv")
OUTPUT_FILE    = os.path.join(DATA_FOLDER, "var_results.csv")

# --- Parameters ---
CONFIDENCE_LEVEL = 0.95            # 95% confidence level
ALPHA            = 1 - CONFIDENCE_LEVEL   # Alpha = 5% (the loss tail)
N_SIMULATIONS    = 10_000          # Number of Monte Carlo simulations

# Set a random seed for reproducibility (so results are the same each time)
np.random.seed(42)

# =============================================================================
# STEP 1: LOAD PORTFOLIO RETURNS
# =============================================================================

print("=" * 60)
print("VALUE AT RISK (VaR) CALCULATIONS")
print(f"Confidence level: {CONFIDENCE_LEVEL*100:.0f}%  |  Horizon: 1 day")
print("=" * 60)

if not os.path.exists(INPUT_FILE):
    print("ERROR: portfolio_returns.csv not found. Please run 04_portfolio.py first.")
    exit()

portfolio_returns = pd.read_csv(INPUT_FILE, index_col="Date", parse_dates=True)
portfolio_returns = portfolio_returns.squeeze()   # Convert from DataFrame to Series

print(f"\nPortfolio returns loaded: {len(portfolio_returns)} daily observations")
print(f"Date range: {portfolio_returns.index[0].date()} to {portfolio_returns.index[-1].date()}")

# Key statistics (inputs for all 3 methods)
mean_return = portfolio_returns.mean()
std_return  = portfolio_returns.std()

print(f"\nKey inputs:")
print(f"  Mean daily return       : {mean_return:.6f} ({mean_return*100:.4f}%)")
print(f"  Standard deviation      : {std_return:.6f} ({std_return*100:.4f}%)")

# =============================================================================
# METHOD 1: HISTORICAL VaR
# =============================================================================
# We sort all past returns and take the 5th percentile.
# No mathematical model is assumed - we rely purely on history.

print("\n" + "-" * 40)
print("METHOD 1: HISTORICAL VaR")

# numpy percentile: 5th percentile of all historical returns
# This is the threshold below which 5% of daily returns fall
historical_var = np.percentile(portfolio_returns, ALPHA * 100)

# VaR is usually expressed as a positive number representing a loss
# If historical_var is -0.015, we report the VaR as 1.5%
print(f"  Historical VaR (95%, 1-day) : {-historical_var*100:.4f}%")
print(f"  Interpretation: On 95% of trading days, the daily loss is less than {-historical_var*100:.2f}%")

# =============================================================================
# METHOD 2: PARAMETRIC VaR (Variance-Covariance)
# =============================================================================
# We assume returns follow a Normal (bell curve) distribution.
# We use the mean and standard deviation of historical returns.
# Formula: VaR = -(mean + z * std)   where z = -1.645 for 95% confidence

print("\n" + "-" * 40)
print("METHOD 2: PARAMETRIC VaR (Normal distribution assumed)")

# The z-score for a 95% confidence level is -1.645
# (i.e., 5% of a normal distribution lies below -1.645 standard deviations)
z_score = stats.norm.ppf(ALPHA)   # ppf = percent point function (inverse of CDF)

parametric_var = mean_return + z_score * std_return

print(f"  Z-score at 5% tail      : {z_score:.4f}")
print(f"  Parametric VaR (95%, 1-day) : {-parametric_var*100:.4f}%")
print(f"  Interpretation: Assuming normal returns, daily loss exceeds {-parametric_var*100:.2f}% only 5% of the time")

# =============================================================================
# METHOD 3: MONTE CARLO VaR
# =============================================================================
# We randomly simulate 10,000 possible future returns.
# Each simulated return is drawn from a normal distribution with the
# same mean and std as our historical data.
# Then we take the 5th percentile of these simulated outcomes.

print("\n" + "-" * 40)
print(f"METHOD 3: MONTE CARLO VaR ({N_SIMULATIONS:,} simulations)")

# Generate 10,000 random returns from a normal distribution
simulated_returns = np.random.normal(loc=mean_return, scale=std_return, size=N_SIMULATIONS)

# Take the 5th percentile of the simulations
monte_carlo_var = np.percentile(simulated_returns, ALPHA * 100)

print(f"  Monte Carlo VaR (95%, 1-day) : {-monte_carlo_var*100:.4f}%")
print(f"  Interpretation: Based on {N_SIMULATIONS:,} random scenarios, daily loss exceeds {-monte_carlo_var*100:.2f}% only 5% of the time")

# =============================================================================
# COMPARISON SUMMARY
# =============================================================================

print("\n" + "=" * 60)
print("COMPARISON SUMMARY - VaR AT 95% CONFIDENCE (1-DAY HORIZON)")
print("=" * 60)

results = {
    "Method": ["Historical VaR", "Parametric VaR", "Monte Carlo VaR"],
    "VaR (%)": [
        round(-historical_var * 100, 4),
        round(-parametric_var * 100, 4),
        round(-monte_carlo_var * 100, 4)
    ]
}

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

print("""
How to interpret this table:
  - All three methods estimate the 1-day 95% VaR of your portfolio.
  - A VaR of 1.5% means: "I do not expect to lose more than 1.5% in one day,
    on 95% of trading days."
  - Differences between methods reveal their assumptions:
      * Historical: uses only past data, no distribution assumption
      * Parametric: faster but assumes returns are normally distributed
      * Monte Carlo: simulates random outcomes, very flexible
  - In practice, if returns are not perfectly normal (fat tails, skewness),
    Historical VaR will often be larger (more conservative) than Parametric.
""")

# =============================================================================
# SAVE RESULTS
# =============================================================================

results_df.to_csv(OUTPUT_FILE, index=False)

# Also save the Monte Carlo simulations (useful for the visualization script)
sim_df = pd.Series(simulated_returns, name="Simulated_Returns")
sim_df.to_csv(os.path.join(DATA_FOLDER, "mc_simulations.csv"), index=False)

print(f"VaR results saved to: {OUTPUT_FILE}")
print(f"Monte Carlo simulations saved for visualization.")
print("You can now run script 06_visualizations.py")
