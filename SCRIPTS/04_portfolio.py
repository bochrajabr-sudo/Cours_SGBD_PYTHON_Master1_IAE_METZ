# =============================================================================
# SCRIPT 04 - BUILD THE EQUALLY WEIGHTED PORTFOLIO
# =============================================================================
# PURPOSE:
#   This script combines the individual stock returns into a single portfolio
#   return series. We use an equally weighted portfolio, which means each
#   stock gets the same share of the total investment.
#
# WHAT IS AN EQUALLY WEIGHTED PORTFOLIO?
#   If we invest $10,000 total across 5 stocks, each stock gets $2,000 (20%).
#   The portfolio return each day is simply the average of all stock returns.
#
#   Portfolio Return = (1/5) * Return_LVMUY + (1/5) * Return_JNJ + ...
#
#   This is the simplest form of diversification. It is also the most
#   transparent and easy to explain in a class presentation.
#
# WHAT IS DIVERSIFICATION?
#   By combining stocks from different sectors, we reduce the risk.
#   When one sector falls (e.g., tech), another may hold steady (e.g., defense).
#   This is one of the key ideas in modern portfolio theory.
#
# WHAT IT DOES STEP BY STEP:
#   1. Load the individual stock returns
#   2. Define equal weights (20% each)
#   3. Compute the daily portfolio return
#   4. Simulate a portfolio value starting at $10,000
#   5. Save the portfolio returns and value to CSV files
# =============================================================================

# --- Import libraries ---
import pandas as pd    # For data manipulation
import numpy as np     # For numerical computations
import os              # For file paths

# --- Define paths ---
DATA_FOLDER         = os.path.join(os.path.dirname(__file__), "..", "DATA")
INPUT_FILE          = os.path.join(DATA_FOLDER, "returns.csv")
OUTPUT_RETURNS      = os.path.join(DATA_FOLDER, "portfolio_returns.csv")
OUTPUT_VALUE        = os.path.join(DATA_FOLDER, "portfolio_value.csv")

# =============================================================================
# STEP 1: LOAD INDIVIDUAL STOCK RETURNS
# =============================================================================

print("=" * 60)
print("BUILDING THE EQUALLY WEIGHTED PORTFOLIO")
print("=" * 60)

if not os.path.exists(INPUT_FILE):
    print("ERROR: returns.csv not found. Please run 03_compute_returns.py first.")
    exit()

returns = pd.read_csv(INPUT_FILE, index_col="Date", parse_dates=True)
print(f"\nLoaded returns for {returns.shape[1]} stocks over {returns.shape[0]} days")
print(f"Stocks: {list(returns.columns)}")

# =============================================================================
# STEP 2: DEFINE EQUAL WEIGHTS
# =============================================================================

n_stocks = len(returns.columns)

# Each stock gets an equal share of the portfolio
# For 5 stocks: each weight = 1/5 = 0.20 = 20%
weights = np.array([1 / n_stocks] * n_stocks)

print(f"\nNumber of stocks: {n_stocks}")
print(f"Weight per stock: {weights[0]:.2%} (equally weighted)")
print(f"Weights sum to: {weights.sum():.2f} (should be 1.0)")

# =============================================================================
# STEP 3: COMPUTE DAILY PORTFOLIO RETURN
# =============================================================================

# Portfolio return = weighted average of individual stock returns
# dot() multiplies each return by its weight and sums them up
portfolio_returns = returns.dot(weights)
portfolio_returns.name = "Portfolio_Return"

print(f"\nPortfolio return statistics:")
print(f"  Mean daily return : {portfolio_returns.mean():.4f} ({portfolio_returns.mean()*100:.2f}%)")
print(f"  Std deviation     : {portfolio_returns.std():.4f} ({portfolio_returns.std()*100:.2f}%)")
print(f"  Worst day         : {portfolio_returns.min():.4f} ({portfolio_returns.min()*100:.2f}%)")
print(f"  Best day          : {portfolio_returns.max():.4f} ({portfolio_returns.max()*100:.2f}%)")

# =============================================================================
# STEP 4: SIMULATE PORTFOLIO VALUE (starting at $10,000)
# =============================================================================

# We simulate how $10,000 invested at the start would have evolved over time.
# Each day: new_value = previous_value * (1 + daily_return)
INITIAL_VALUE = 10_000   # Starting investment in US dollars

# cumprod() computes the cumulative product over time
portfolio_value = INITIAL_VALUE * (1 + portfolio_returns).cumprod()
portfolio_value.name = "Portfolio_Value"

final_value = portfolio_value.iloc[-1]
total_return = (final_value - INITIAL_VALUE) / INITIAL_VALUE * 100

print(f"\nPortfolio simulation (starting at ${INITIAL_VALUE:,}):")
print(f"  Final value       : ${final_value:,.2f}")
print(f"  Total return      : {total_return:.2f}%")

# =============================================================================
# STEP 5: SAVE RESULTS
# =============================================================================

portfolio_returns.to_csv(OUTPUT_RETURNS)
portfolio_value.to_csv(OUTPUT_VALUE)

print(f"\nPortfolio returns saved to : {OUTPUT_RETURNS}")
print(f"Portfolio value saved to   : {OUTPUT_VALUE}")
print("You can now run script 05_var_calculations.py")
