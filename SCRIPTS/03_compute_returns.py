# =============================================================================
# SCRIPT 03 - COMPUTE DAILY RETURNS
# =============================================================================
# PURPOSE:
#   This script takes the clean price data and computes the daily returns
#   for each stock. Returns are the fundamental input for any risk analysis.
#
# WHAT IS A DAILY RETURN?
#   A return measures how much the price changed from one day to the next.
#   We use "simple returns" (percentage change), which is the most intuitive:
#
#       Return on day t = (Price on day t - Price on day t-1) / Price on day t-1
#
#   For example: if a stock was $100 yesterday and $103 today, the return is +3%.
#
# WHY DO WE NEED RETURNS (AND NOT PRICES)?
#   - Returns are stationary (they don't trend upward like prices)
#   - They measure actual gain or loss, which is what risk is about
#   - They allow us to compare stocks regardless of their price level
#
# WHAT IT DOES STEP BY STEP:
#   1. Load the clean price file
#   2. Compute daily percentage returns for each stock
#   3. Display basic statistics (mean, std, min, max)
#   4. Save the returns to a CSV file
# =============================================================================

# --- Import libraries ---
import pandas as pd    # For data manipulation
import os              # For file paths

# --- Define paths ---
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "DATA")
INPUT_FILE  = os.path.join(DATA_FOLDER, "prices_clean.csv")
OUTPUT_FILE = os.path.join(DATA_FOLDER, "returns.csv")

# =============================================================================
# STEP 1: LOAD CLEAN PRICE DATA
# =============================================================================

print("=" * 60)
print("COMPUTING DAILY RETURNS")
print("=" * 60)

# Check the input file exists
if not os.path.exists(INPUT_FILE):
    print("ERROR: prices_clean.csv not found. Please run 02_clean_data.py first.")
    exit()

# Load the clean prices
prices = pd.read_csv(INPUT_FILE, index_col="Date", parse_dates=True)
print(f"\nPrices loaded: {prices.shape[0]} days, {prices.shape[1]} stocks")

# =============================================================================
# STEP 2: COMPUTE DAILY RETURNS
# =============================================================================

# pct_change() computes: (today - yesterday) / yesterday
# The first row becomes NaN because there is no previous day -> we drop it
returns = prices.pct_change().dropna()

print(f"Returns computed: {returns.shape[0]} daily observations per stock")

# =============================================================================
# STEP 3: DISPLAY BASIC STATISTICS
# =============================================================================

print("\n--- Descriptive Statistics for Daily Returns ---")
print("(Values are in decimal form: 0.01 = +1%, -0.02 = -2%)\n")

stats = returns.describe()
print(stats.round(4))

# Interpretation guide printed to the console
print("\n--- How to read these statistics ---")
print("  mean  : average daily return (how much you earn on average per day)")
print("  std   : standard deviation (measures volatility / risk)")
print("  min   : worst single day loss in the period")
print("  max   : best single day gain in the period")
print("  25%   : on 25% of days, return was below this value")
print("  75%   : on 75% of days, return was below this value")

# =============================================================================
# STEP 4: SAVE RETURNS
# =============================================================================

returns.to_csv(OUTPUT_FILE)
print(f"\nReturns saved to: {OUTPUT_FILE}")
print("You can now run script 04_portfolio.py")
