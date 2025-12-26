import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION & DATA EXTRACTION
# ==========================================
print(">>> Starting Portfolio Optimization Engine...")

# List of assets to analyze (Diversified Tech, Finance, Energy, Gold)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'JPM', 'XOM', 'GLD', 'TSLA', 'AMZN']
risk_free_rate = 0.04  # Assuming 4% risk-free rate (approx. US Treasury Yield)

# Define date range: Historical data for the last 2 years
end_date = datetime.today()
start_date = end_date - timedelta(days=365*2)

print(f"Downloading data for: {tickers}...")

# FETCH DATA FIX: 
# We use 'auto_adjust=True' so Yahoo returns prices already adjusted for splits/dividends.
# This prevents the 'KeyError: Adj Close' issue.
raw_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)

# Select only the 'Close' column (which is effectively the Adjusted Close now)
data = raw_data['Close']

# Check for missing values and fill them using forward fill method
if data.isnull().values.any():
    print("Warning: Missing data detected. Filling with forward method.")
    data = data.ffill()

print("Data successfully downloaded and cleaned.")

# ==========================================
# 2. FINANCIAL CALCULATIONS (RETURNS & RISK)
# ==========================================
# Calculate Logarithmic Returns (Standard for time-series analysis)
log_returns = np.log(data / data.shift(1)).dropna()

# Calculate Annualized Covariance Matrix
# 252 is the standard number of trading days in a year
cov_matrix = log_returns.cov() * 252

print("Calculating Efficient Frontier via Monte Carlo Simulation...")

# ==========================================
# 3. MONTE CARLO SIMULATION
# ==========================================
num_portfolios = 10000
results = np.zeros((3, num_portfolios))  # Array to store [Return, Volatility, Sharpe Ratio]
weights_record = []  # List to store weight allocations for each simulation

for i in range(num_portfolios):
    # Generate random weights for each asset
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)  # Normalize weights so they sum to 1 (100%)
    weights_record.append(weights)
    
    # Calculate Expected Portfolio Return (Annualized)
    port_return = np.sum(log_returns.mean() * weights) * 252
    
    # Calculate Expected Portfolio Volatility (Risk)
    # Formula: sqrt(w.T * CovMatrix * w)
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Calculate Sharpe Ratio (Risk-Adjusted Return)
    sharpe_ratio = (port_return - risk_free_rate) / port_volatility
    
    # Store results
    results[0, i] = port_return
    results[1, i] = port_volatility
    results[2, i] = sharpe_ratio

# ==========================================
# 4. OPTIMIZATION RESULT
# ==========================================
# Identify the index of the portfolio with the Maximum Sharpe Ratio
max_sharpe_idx = np.argmax(results[2])

# Extract stats for the optimal portfolio
optimal_volatility = results[1, max_sharpe_idx]
optimal_return = results[0, max_sharpe_idx]
optimal_sharpe = results[2, max_sharpe_idx]

# Create a DataFrame for the optimal weights
max_sharpe_allocation = pd.DataFrame(
    weights_record[max_sharpe_idx], 
    index=tickers, 
    columns=['Allocation']
)
# Format allocation as percentages
max_sharpe_allocation.Allocation = [round(i*100, 2) for i in max_sharpe_allocation.Allocation]

print("\n------------------------------------------------")
print("🏆 OPTIMAL PORTFOLIO (Max Sharpe Ratio)")
print("------------------------------------------------")
print(f"Annual Return:     {optimal_return:.2%}")
print(f"Annual Volatility: {optimal_volatility:.2%}")
print(f"Sharpe Ratio:      {optimal_sharpe:.2f}")
print("\nSuggested Asset Allocation (%):")
print(max_sharpe_allocation.sort_values(by='Allocation', ascending=False))
print("------------------------------------------------")

# ==========================================
# 5. VISUALIZATION (EFFICIENT FRONTIER)
# ==========================================
plt.figure(figsize=(12, 8))

# Scatter plot of all simulated portfolios
# X-axis: Risk (Volatility), Y-axis: Return, Color: Sharpe Ratio
plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='viridis', marker='o', s=10, alpha=0.5)
plt.colorbar(label='Sharpe Ratio')

# Highlight the Optimal Portfolio (Red Star)
plt.scatter(optimal_volatility, optimal_return, marker='*', color='red', s=500, label='Max Sharpe Ratio')

# Chart formatting
plt.title('Markowitz Efficient Frontier (Monte Carlo Simulation)')
plt.xlabel('Annualized Volatility (Risk)')
plt.ylabel('Annualized Return')
plt.legend(labelspacing=0.8)
plt.grid(True, linestyle='--', alpha=0.6)

# Save the plot
output_filename = "efficient_frontier.png"
plt.savefig(output_filename)
print(f"\n>>> Chart saved as '{output_filename}'. Check your project folder!")

# Show the plot
plt.show()

# ==========================================
# 6. EXPORT DATA FOR POWER BI
# ==========================================
print("\nExporting simulation data to CSV...")

# Create a DataFrame with all simulation results
portfolio_data = pd.DataFrame({
    'Volatility': results[1, :],
    'Return': results[0, :],
    'Sharpe_Ratio': results[2, :]
})

# Save to CSV
portfolio_data.to_csv('markowitz_simulation.csv', index=False)

# Save the Optimal Weights separately (for the Donut Chart)
max_sharpe_allocation.to_csv('optimal_weights.csv')

print(">>> Files 'markowitz_simulation.csv' and 'optimal_weights.csv' created successfully.")