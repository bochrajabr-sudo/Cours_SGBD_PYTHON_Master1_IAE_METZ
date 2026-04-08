# =============================================================================
# MAIN SCRIPT - RUNS THE ENTIRE PROJECT IN ORDER
# =============================================================================
# PURPOSE:
#   This script executes all 6 project scripts one by one, in the correct order.
#   You can run this single file to reproduce the entire analysis from scratch.
#
# HOW TO RUN:
#   Open a terminal, navigate to the SCRIPTS folder, and type:
#       python main.py
#
# WHAT HAPPENS:
#   Step 1 -> Download stock data from Yahoo Finance    (01_download_data.py)
#   Step 2 -> Clean and inspect the data               (02_clean_data.py)
#   Step 3 -> Compute daily returns                    (03_compute_returns.py)
#   Step 4 -> Build the equally weighted portfolio     (04_portfolio.py)
#   Step 5 -> Calculate Historical, Parametric,
#             and Monte Carlo VaR                      (05_var_calculations.py)
#   Step 6 -> Generate all visualizations              (06_visualizations.py)
#
# NOTE:
#   Each script can also be run independently if needed.
#   Running main.py is simply a shortcut to run them all at once.
# =============================================================================

import subprocess   # To run other Python scripts from this script
import sys          # To get the current Python interpreter path
import os           # For file paths

# Get the directory where this script is located (i.e., the SCRIPTS folder)
SCRIPTS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# List of scripts to run, in order
SCRIPTS = [
    "01_download_data.py",
    "02_clean_data.py",
    "03_compute_returns.py",
    "04_portfolio.py",
    "05_var_calculations.py",
    "06_visualizations.py"
]

# =============================================================================
# RUN EACH SCRIPT IN ORDER
# =============================================================================

print("=" * 60)
print("VALUE AT RISK PROJECT - FULL PIPELINE")
print("Running all scripts in order...")
print("=" * 60)

for i, script_name in enumerate(SCRIPTS, start=1):
    script_path = os.path.join(SCRIPTS_FOLDER, script_name)

    print(f"\n[{i}/{len(SCRIPTS)}] Running: {script_name}")
    print("-" * 50)

    # Run the script using the same Python interpreter as main.py
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=False   # Show output directly in the terminal
    )

    # Check if the script ran successfully
    if result.returncode != 0:
        print(f"\nERROR: Script '{script_name}' failed with return code {result.returncode}")
        print("Please check the error message above and fix the issue before continuing.")
        sys.exit(1)   # Stop the pipeline if a script fails
    else:
        print(f"\n[{i}/{len(SCRIPTS)}] '{script_name}' completed successfully.")

# =============================================================================
# FINAL MESSAGE
# =============================================================================

print("\n" + "=" * 60)
print("PROJECT PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)
print("""
All steps have been executed. Here is a summary of outputs:

DATA/ folder contains:
  - LVMUY.csv, JNJ.csv, LMT.csv, NEE.csv, AAPL.csv  -> Raw stock data
  - prices_clean.csv                                  -> Clean adjusted close prices
  - returns.csv                                       -> Individual stock returns
  - portfolio_returns.csv                             -> Daily portfolio returns
  - portfolio_value.csv                               -> Portfolio value over time
  - var_results.csv                                   -> VaR results (all 3 methods)
  - mc_simulations.csv                                -> Monte Carlo simulation data
  - chart1_stock_performance.png                      -> Comparative performance chart
  - chart2_portfolio_value.png                        -> Portfolio evolution chart
  - chart3_return_distribution.png                    -> Return distribution histogram
  - chart4_var_comparison.png                         -> VaR comparison chart

You can now use the charts and var_results.csv for your presentation!
""")
