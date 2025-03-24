import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# My results from backtesting the SMA strategy
# Total Trades: 47
# Peak Equit: 189%
# Final Equity: 177%
# Max Drawdown: -20/9%
# Max Drawdown Duration: 742 days

np.random.seed(42)
dates = pd.date_range(start = "2004-08-20", periods = 1000, freq = "D")
returns = np.random.normal(0.0005, 0.02, 1000)
equity_curve = 100000 * (1 + returns).cumprod()

# Creating the DataFrame and setting the date index
df = pd.DataFrame({
    'Date': dates,
    'Equity': equity_curve,
    'Returns': returns
})

# Plot the equity curve
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Equity'], label = "Equity Curve", color = "blue", linewidth = 2)
plt.xlabel("Date")
plt.ylabel("Equity Value")
plt.title("Backtesting Equity Curve (Peak 189%, Final 177%")
plt.legend()
plt.grid()
plt.show()

# Plot the Returns Distribution (Histogram)
plt.figure(figsize=(12, 6))
plt.hist(df['Returns'], bins=50, color='purple', alpha=0.7)  # purple looks nice
plt.xlabel("Daily Returns")
plt.ylabel("Frequency")
plt.title("Distribution of Returns")
plt.grid()
plt.show()

# Calculating the Drawdown
df['Peak'] = df['Equity'].cummax()  # Track the peak equity over time
df['Drawdown'] = (df['Equity'] - df['Peak']) / df['Peak']  # Calculate relative drawdown

# Plot Drawdown Over Time (Max Drawdown: -20.9%)
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Drawdown'], label="Drawdown", color="red", linewidth=2)
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")
plt.title("Drawdown Over Time (Max Drawdown: -20.9%)")
plt.legend()
plt.grid()
plt.show()

# Additional info can be noted or computed
max_dd_duration = (df['Drawdown'] < 0).astype(int).groupby(df['Drawdown'].ne(0).cumsum()).cumsum().max()
print(f"Max Drawdown Duration: {max_dd_duration} days")