# =============================================================================
# SCRIPT 01 - DOWNLOAD DATA FROM YAHOO FINANCE
# =============================================================================
# PURPOSE:
#   This script downloads historical stock price data from Yahoo Finance
#   using the yfinance library. The data is saved as CSV files in the DATA/
#   folder so that other scripts can load it without downloading again.
#
# WHAT IT DOES STEP BY STEP:
#   1. Define the list of stocks we want to analyze
#   2. Set the date range for our data
#   3. Download the data using yfinance
#   4. Save each stock's data as a separate CSV file
# =============================================================================

# --- Import libraries ---
import yfinance as yf      # To download data from Yahoo Finance
import os                  # To create folders if they don't exist

# --- Define our stock portfolio ---
# We chose 5 US-listed stocks, one per sector, for diversification.
# Each stock is a well-known company that is easy to explain in class.

STOCKS = {
    "LVMUY": "Luxury       - LVMH (world's largest luxury goods group)",
    "JNJ":   "Healthcare   - Johnson & Johnson (pharma and medical devices)",
    "LMT":   "Defense      - Lockheed Martin (leading US defense contractor)",
    "NEE":   "Renewable    - NextEra Energy (largest US renewable energy company)",
    "AAPL":  "Technology   - Apple (most valuable tech company in the world)"
}

# --- Define the date range ---
# We use 5 years of daily data: from 2020 to 2024.
# This gives us about 1250 trading days, which is enough for a solid analysis.
# Using 5 years also captures a crisis period (COVID-2020), which makes the
# risk analysis more interesting academically.

START_DATE = "2020-01-01"
END_DATE   = "2024-12-31"

# --- Define where to save the data ---
# This path goes up one folder from SCRIPTS/ and into DATA/
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "DATA")

# Create the DATA folder if it does not already exist
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Download and save each stock ---
print("=" * 60)
print("DOWNLOADING STOCK DATA FROM YAHOO FINANCE")
print("=" * 60)
print(f"Date range: {START_DATE} to {END_DATE}")
print(f"Stocks selected:\n")
for ticker, description in STOCKS.items():
    print(f"  {ticker} -> {description}")
print()

for ticker in STOCKS:
    print(f"Downloading {ticker}...")

    # Download data for this stock
    # yf.download returns a DataFrame with columns like:
    # Open, High, Low, Close, Adj Close, Volume
    data = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=False)

    # Check that data was actually downloaded
    if data.empty:
        print(f"  WARNING: No data returned for {ticker}. Please check the ticker symbol.")
        continue

    # Save the data to a CSV file in the DATA folder
    output_file = os.path.join(DATA_FOLDER, f"{ticker}.csv")
    data.to_csv(output_file)

    print(f"  Saved: {output_file} ({len(data)} rows)")

print()
print("Download complete. All files are saved in the DATA/ folder.")
print("You can now run script 02_clean_data.py")
