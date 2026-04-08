# =============================================================================
# SCRIPT 02 - INSPECT AND CLEAN THE DATA
# =============================================================================
# PURPOSE:
#   This script loads the raw CSV files downloaded by script 01,
#   inspects their quality, handles any missing values, and saves
#   a clean combined file with only the "Adj Close" price column.
#
# WHY "ADJ CLOSE" AND NOT "CLOSE"?
#   "Adj Close" (Adjusted Close) corrects for events like dividends and
#   stock splits. This makes the price series comparable over time and
#   more accurate for computing returns. It is the standard choice in
#   academic finance.
#
# WHAT IT DOES STEP BY STEP:
#   1. Load each CSV file from the DATA/ folder
#   2. Display basic information (shape, missing values, first rows)
#   3. Keep only the "Adj Close" column
#   4. Align all stocks on the same dates (inner join)
#   5. Handle any remaining missing values
#   6. Save the clean combined file as "prices_clean.csv"
# =============================================================================

# --- Import libraries ---
import pandas as pd    # For loading and manipulating data tables
import os              # For file paths

# --- Define paths ---
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "DATA")

# List of our 5 tickers (must match the files created by script 01)
TICKERS = ["LVMUY", "JNJ", "LMT", "NEE", "AAPL"]

# =============================================================================
# STEP 1: LOAD EACH FILE AND INSPECT IT
# =============================================================================

print("=" * 60)
print("LOADING AND INSPECTING RAW DATA")
print("=" * 60)

adj_close_dict = {}   # Dictionary to store each stock's Adj Close series

for ticker in TICKERS:
    file_path = os.path.join(DATA_FOLDER, f"{ticker}.csv")

    # Check the file exists
    if not os.path.exists(file_path):
        print(f"ERROR: File not found for {ticker}. Please run 01_download_data.py first.")
        continue

    # Load the CSV. The first column is the date (used as index).
    df = pd.read_csv(file_path, index_col=0, parse_dates=True, header=[0, 1])

    # yfinance saves a multi-level header. We flatten it here.
    # After this, columns will be: Open, High, Low, Close, Adj Close, Volume
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    print(f"\n--- {ticker} ---")
    print(f"  Rows: {len(df)} | Columns: {list(df.columns)}")
    print(f"  Date range: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"  Missing values:\n{df.isnull().sum()}")

    # Keep only "Adj Close"
    if "Adj Close" in df.columns:
        adj_close_dict[ticker] = df["Adj Close"]
    else:
        print(f"  WARNING: 'Adj Close' column not found for {ticker}!")

# =============================================================================
# STEP 2: COMBINE ALL STOCKS INTO ONE TABLE
# =============================================================================

print("\n" + "=" * 60)
print("COMBINING ALL STOCKS INTO ONE CLEAN TABLE")
print("=" * 60)

# Create a single DataFrame with one column per stock
# how="inner" means we only keep dates where ALL stocks have a price
# This automatically removes weekends and holidays
prices = pd.DataFrame(adj_close_dict)
prices.index.name = "Date"

print(f"\nCombined table shape: {prices.shape}")
print(f"Date range: {prices.index[0].date()} to {prices.index[-1].date()}")

# =============================================================================
# STEP 3: HANDLE MISSING VALUES
# =============================================================================

print(f"\nMissing values before cleaning:\n{prices.isnull().sum()}")

# Forward fill: if a value is missing on a day, use the previous day's price.
# This is a standard practice for stock data (e.g., public holidays).
prices.ffill(inplace=True)

# Drop any remaining rows with missing values (e.g., at the very start)
prices.dropna(inplace=True)

print(f"Missing values after cleaning:\n{prices.isnull().sum()}")
print(f"\nFinal table shape after cleaning: {prices.shape}")

# =============================================================================
# STEP 4: SAVE THE CLEAN FILE
# =============================================================================

output_file = os.path.join(DATA_FOLDER, "prices_clean.csv")
prices.to_csv(output_file)

print(f"\nClean data saved to: {output_file}")
print("You can now run script 03_compute_returns.py")
print("\nFirst 5 rows of clean data:")
print(prices.head())
