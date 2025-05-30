# delta-hedging-simulator

Delta Hedging Simulator

This project implements a Delta Hedging simulation using historical price data for a listed security (e.g., AAPL) and models the P&L of a dynamically hedged options portfolio over time. It applies quantitative finance concepts like the Black-Scholes model, Greeks, and discrete rebalancing under realistic conditions (e.g., transaction costs, finite hedging frequency).

Core Concepts
	•	Delta Hedging: A strategy that neutralizes directional risk by taking offsetting positions in the underlying asset and its derivative (option), based on the option’s delta.
	•	Black-Scholes Pricing: Closed-form pricing of European options assuming log-normal asset returns, continuous trading, and constant volatility.
	•	Historical Volatility Estimation: Realized volatility is estimated from log returns of adjusted close prices, annualized using √252 scaling.
	•	Path-Dependent P&L: The hedging error evolves based on how frequently and how accurately the portfolio is rebalanced.

⸻

Features
	•	Real Data Simulation: Pulls real stock data via yfinance, normalizes the path to [0, 1] time scale.
	•	Delta Rebalancing: Implements discrete hedging intervals (every n steps) with cash and asset position updates.
	•	Transaction Costs: Models proportional costs (default: 0.1%) per trade to reflect realistic execution slippage.
	•	Volatility Estimation: Computes historical volatility using daily log returns.
	•	Greeks Tracking: Logs delta values at each timestep and visualizes their time evolution.
	•	Interactive Plots:
	•	Normalized asset price path
	•	Delta over time
	•	Hedged portfolio P&L trajectory

⸻

Example Output

Figure: Delta-Hedged Portfolio Value Over Time

Figure: Delta Evolution Across Time

⸻

How It Works

Load historical price data (auto-adjusted)
data = yf.download("AAPL", start="2024-01-01", end="2024-12-31", auto_adjust=True)

Estimate annualized historical volatility
sigma = np.std(np.log(data['Close'] / data['Close'].shift(1))) * np.sqrt(252)

Normalize price path to 0–1 scale and simulate
path = normalize_price_series(data['Close'])
portfolio, deltas = simulate_delta_hedging(path, K=S0, r=0.0443, sigma=sigma)



Future Improvements
	•	Incorporate gamma risk and higher-order Greeks
	•	Model stochastic volatility (e.g., using GARCH or SABR models)
	•	Add multi-asset support or portfolio-level hedging
	•	Backtest across multiple assets with rolling window calibration

⸻

References
	•	Hull, J. (2022). Options, Futures, and Other Derivatives
	•	Black, F., & Scholes, M. (1973). The Pricing of Options and Corporate Liabilities
	•	Wilmott, P. (2006). Paul Wilmott Introduces Quantitative Finance

⸻

Requirements

pip install numpy pandas matplotlib yfinance scipy


⸻

📌 License

MIT License. Feel free to fork, extend, and contribute!

