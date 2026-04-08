# =============================================================================
# SCRIPT 06 - VISUALIZATIONS
# =============================================================================
# PURPOSE:
#   This script generates all the charts needed for the project presentation.
#   It creates 4 key charts:
#
#   CHART 1 - Comparative stock performance (normalized to 100 at start)
#             Shows how each stock evolved over the period.
#
#   CHART 2 - Portfolio value evolution
#             Shows how a $10,000 investment would have grown over time.
#
#   CHART 3 - Return distribution (histogram + normal curve)
#             Shows the shape of the portfolio's daily return distribution.
#             Helps visualize the risk profile.
#
#   CHART 4 - VaR comparison chart
#             Shows the return distribution and the three VaR thresholds
#             side by side, so we can compare Historical, Parametric,
#             and Monte Carlo VaR visually.
#
# HOW TO READ THE CHARTS FOR YOUR ORAL PRESENTATION:
#   - Chart 1: "We can see that [stock X] outperformed others over the period."
#   - Chart 2: "Our portfolio grew from $10,000 to $X, but also suffered during..."
#   - Chart 3: "The distribution is roughly bell-shaped, with a slight left tail."
#   - Chart 4: "The three VaR methods give similar results. Historical VaR
#               is slightly more conservative because it captures real market events."
# =============================================================================

# --- Import libraries ---
import pandas as pd              # For data manipulation
import numpy as np               # For numerical computations
import matplotlib.pyplot as plt  # For creating charts
import matplotlib.patches as mpatches  # For custom legend items
from scipy import stats          # For the normal distribution curve
import os                        # For file paths

# --- Define paths ---
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "DATA")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "..", "DATA")

# --- Visual style ---
plt.style.use("seaborn-v0_8-whitegrid")   # Clean academic look
COLORS = ["#2196F3", "#4CAF50", "#F44336", "#FF9800", "#9C27B0"]
# Blue = LVMUY, Green = JNJ, Red = LMT, Orange = NEE, Purple = AAPL

# =============================================================================
# LOAD ALL DATA
# =============================================================================

print("=" * 60)
print("GENERATING VISUALIZATIONS")
print("=" * 60)

# Load clean prices
prices = pd.read_csv(os.path.join(DATA_FOLDER, "prices_clean.csv"),
                     index_col="Date", parse_dates=True)

# Load individual stock returns
returns = pd.read_csv(os.path.join(DATA_FOLDER, "returns.csv"),
                      index_col="Date", parse_dates=True)

# Load portfolio returns
portfolio_returns = pd.read_csv(os.path.join(DATA_FOLDER, "portfolio_returns.csv"),
                                index_col="Date", parse_dates=True).squeeze()

# Load portfolio value
portfolio_value = pd.read_csv(os.path.join(DATA_FOLDER, "portfolio_value.csv"),
                               index_col="Date", parse_dates=True).squeeze()

# Load VaR results
var_results = pd.read_csv(os.path.join(DATA_FOLDER, "var_results.csv"))

# Load Monte Carlo simulations
mc_simulations = pd.read_csv(os.path.join(DATA_FOLDER, "mc_simulations.csv")).squeeze()

# Extract VaR values (negative, so we convert to loss)
var_dict = dict(zip(var_results["Method"], var_results["VaR (%)"]))
hist_var_pct    = var_dict["Historical VaR"]
param_var_pct   = var_dict["Parametric VaR"]
mc_var_pct      = var_dict["Monte Carlo VaR"]

print(f"\nVaR values loaded:")
print(f"  Historical  : -{hist_var_pct:.4f}%")
print(f"  Parametric  : -{param_var_pct:.4f}%")
print(f"  Monte Carlo : -{mc_var_pct:.4f}%")

# =============================================================================
# CHART 1 - COMPARATIVE STOCK PERFORMANCE (Normalized)
# =============================================================================
# We normalize all prices to 100 at the start date.
# This allows us to compare stocks regardless of their initial price.
# A value of 120 means the stock is up 20% from the start.

print("\nGenerating Chart 1: Comparative stock performance...")

normalized = (prices / prices.iloc[0]) * 100   # Start everything at 100

fig, ax = plt.subplots(figsize=(12, 6))

tickers    = list(normalized.columns)
labels     = {
    "LVMUY": "LVMUY - LVMH (Luxury)",
    "JNJ":   "JNJ - Johnson & Johnson (Healthcare)",
    "LMT":   "LMT - Lockheed Martin (Defense)",
    "NEE":   "NEE - NextEra Energy (Renewable)",
    "AAPL":  "AAPL - Apple (Technology)"
}

for i, ticker in enumerate(tickers):
    ax.plot(normalized.index, normalized[ticker],
            label=labels.get(ticker, ticker),
            color=COLORS[i], linewidth=1.8)

ax.axhline(y=100, color="black", linestyle="--", linewidth=1, alpha=0.5, label="Base (100)")
ax.set_title("Comparative Stock Performance (Base 100 = January 2020)", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Normalized Price (Base 100)")
ax.legend(loc="upper left", fontsize=9)
ax.tick_params(axis='x', rotation=30)

plt.tight_layout()
chart1_path = os.path.join(OUTPUT_FOLDER, "chart1_stock_performance.png")
plt.savefig(chart1_path, dpi=150)
plt.close()
print(f"  Saved: {chart1_path}")

# =============================================================================
# CHART 2 - PORTFOLIO VALUE EVOLUTION
# =============================================================================
# Shows how $10,000 invested in our equally weighted portfolio would have
# evolved over the analysis period.

print("Generating Chart 2: Portfolio value evolution...")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(portfolio_value.index, portfolio_value,
        color="#1565C0", linewidth=2, label="Portfolio Value ($)")
ax.fill_between(portfolio_value.index, portfolio_value, alpha=0.15, color="#1565C0")
ax.axhline(y=10_000, color="gray", linestyle="--", linewidth=1, label="Initial Investment ($10,000)")

# Highlight the minimum (worst drawdown)
min_idx = portfolio_value.idxmin()
min_val = portfolio_value.min()
ax.annotate(f"Lowest point\n${min_val:,.0f}",
            xy=(min_idx, min_val),
            xytext=(min_idx, min_val - 800),
            fontsize=9, color="red",
            arrowprops=dict(arrowstyle="->", color="red"))

ax.set_title("Portfolio Value Evolution (Equal-Weighted, Initial Investment = $10,000)", fontsize=13, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Value (USD)")
ax.legend(fontsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.tick_params(axis='x', rotation=30)

plt.tight_layout()
chart2_path = os.path.join(OUTPUT_FOLDER, "chart2_portfolio_value.png")
plt.savefig(chart2_path, dpi=150)
plt.close()
print(f"  Saved: {chart2_path}")

# =============================================================================
# CHART 3 - RETURN DISTRIBUTION (Histogram + Normal curve)
# =============================================================================
# Shows the shape of the portfolio's daily return distribution.
# The red vertical line is the Historical VaR threshold.
# The orange curve is the theoretical normal distribution for comparison.

print("Generating Chart 3: Return distribution (histogram)...")

fig, ax = plt.subplots(figsize=(10, 6))

# Draw histogram of actual portfolio returns
n_bins = 60
ax.hist(portfolio_returns * 100, bins=n_bins, density=True,
        color="#42A5F5", edgecolor="white", alpha=0.75, label="Daily Returns (actual)")

# Overlay the normal distribution curve
mu  = portfolio_returns.mean() * 100
sig = portfolio_returns.std() * 100
x   = np.linspace(mu - 4 * sig, mu + 4 * sig, 300)
ax.plot(x, stats.norm.pdf(x, mu, sig), color="darkorange", linewidth=2,
        linestyle="-", label="Normal Distribution (theoretical)")

# Add a vertical line at the Historical VaR level
ax.axvline(x=-hist_var_pct, color="red", linewidth=2, linestyle="--",
           label=f"Historical VaR 95% = -{hist_var_pct:.2f}%")

# Shade the loss tail (left of VaR)
x_tail = np.linspace(mu - 4 * sig, -hist_var_pct, 200)
ax.fill_between(x_tail, stats.norm.pdf(x_tail, mu, sig),
                color="red", alpha=0.20, label="5% loss tail")

ax.set_title("Distribution of Daily Portfolio Returns (2020-2024)", fontsize=13, fontweight="bold")
ax.set_xlabel("Daily Return (%)")
ax.set_ylabel("Density")
ax.legend(fontsize=9)

plt.tight_layout()
chart3_path = os.path.join(OUTPUT_FOLDER, "chart3_return_distribution.png")
plt.savefig(chart3_path, dpi=150)
plt.close()
print(f"  Saved: {chart3_path}")

# =============================================================================
# CHART 4 - VaR COMPARISON (all 3 methods on one chart)
# =============================================================================
# This chart shows the three VaR thresholds on the same histogram,
# so we can visually compare the three methods.

print("Generating Chart 4: VaR comparison chart...")

fig, ax = plt.subplots(figsize=(11, 6))

# Histogram of actual returns
ax.hist(portfolio_returns * 100, bins=n_bins, density=True,
        color="#B0BEC5", edgecolor="white", alpha=0.6, label="Daily Returns (actual)")

# Normal curve
ax.plot(x, stats.norm.pdf(x, mu, sig), color="black", linewidth=1.5,
        linestyle="-", alpha=0.6, label="Normal distribution")

# Draw the three VaR thresholds
ax.axvline(x=-hist_var_pct,  color="#E53935", linewidth=2.2, linestyle="--",
           label=f"Historical VaR  = -{hist_var_pct:.2f}%")
ax.axvline(x=-param_var_pct, color="#FB8C00", linewidth=2.2, linestyle="-.",
           label=f"Parametric VaR  = -{param_var_pct:.2f}%")
ax.axvline(x=-mc_var_pct,    color="#8E24AA", linewidth=2.2, linestyle=":",
           label=f"Monte Carlo VaR = -{mc_var_pct:.2f}%")

ax.set_title("Comparison of VaR Methods (95% Confidence, 1-Day Horizon)", fontsize=13, fontweight="bold")
ax.set_xlabel("Daily Return (%)")
ax.set_ylabel("Density")
ax.legend(fontsize=9)

# Add a text annotation explaining the reading
ax.text(0.02, 0.97,
        "Vertical lines = maximum 1-day loss\nat 95% confidence (5% of days exceed this)",
        transform=ax.transAxes, fontsize=8, verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

plt.tight_layout()
chart4_path = os.path.join(OUTPUT_FOLDER, "chart4_var_comparison.png")
plt.savefig(chart4_path, dpi=150)
plt.close()
print(f"  Saved: {chart4_path}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 60)
print("ALL CHARTS GENERATED SUCCESSFULLY")
print("=" * 60)
print(f"""
Charts saved in DATA/ folder:
  - chart1_stock_performance.png
  - chart2_portfolio_value.png
  - chart3_return_distribution.png
  - chart4_var_comparison.png

How to use these charts in your presentation:
  Chart 1 -> Justify your stock selection and show sector diversity
  Chart 2 -> Show how the portfolio performed over time (narrative)
  Chart 3 -> Introduce the concept of risk and the loss distribution
  Chart 4 -> Compare the three VaR methods and discuss their differences
""")
