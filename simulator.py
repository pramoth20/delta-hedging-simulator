import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- Simulate GBM Stock Price Path ---
# S0 = Initial stock price
# mu = Expected return
# sigma = Volatility
# T = Time horizon (in years)
# steps = Number of time steps in the simulation
# seed = Random seed for reproducibility
def simulate_gbm(S0, mu, sigma, T, steps, seed=None):
    if seed:
        np.random.seed(seed)

    dt = T / steps
    time_grid = np.linspace(0, T, steps + 1)
    prices = [S0]

    for _ in range(steps):
        Z = np.random.normal()
        S_prev = prices[-1]
        S_next = S_prev * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z) # Geometric Brownian Motion formula
        prices.append(S_next)

    return pd.Series(prices, index=time_grid)

# --- Black-Scholes Formula for Call Option ---
# S = Current stock price
# K = Strike price
# T = Time to expiration (in years)
# r = Risk-free interest rate
# sigma = Volatility of the stock
def black_scholes_call(S, K, T, r, sigma):
    if T <= 0:
        return max(S - K, 0), 1.0 if S > K else 0.0  # Expired option

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1)

    return call_price, delta

# --- Delta Hedging Simulation ---
def simulate_delta_hedging(path, K, r, sigma, hedge_every=5, transaction_cost=0.001):
    steps = len(path) - 1
    dt = 1 / steps
    cash = 0.0
    shares_held = 0.0
    portfolio_value = []
    deltas = []

    for i in range(steps + 1):
        S = path.iloc[i]
        t = i * dt
        T_remaining = 1 - t

        option_price, delta = black_scholes_call(S, K, T_remaining, r, sigma)
        deltas.append(delta)

        if i == 0:
            # Sell the option and buy delta shares to hedge
            trade_amount = delta * S
            cost = abs(trade_amount) * transaction_cost
            cash = option_price - trade_amount - cost
            shares_held = delta
        elif i % hedge_every == 0:
            # Rebalance hedge
            new_shares = delta
            trade_amount = (new_shares - shares_held) * S
            cost = abs(trade_amount) * transaction_cost
            cash -= trade_amount + cost
            shares_held = new_shares

        value = shares_held * S + cash - option_price
        portfolio_value.append(value)

    return pd.Series(portfolio_value, index=path.index), pd.Series(deltas, index=path.index)

# --- MAIN ---
if __name__ == "__main__":
    # Parameters
    S0 = 100
    mu = 0.05
    sigma = 0.2
    T = 1
    steps = 252
    K = 100
    r = 0.01

    # Simulate stock path
    path = simulate_gbm(S0, mu, sigma, T, steps, seed=42)

    # Print initial option price and delta
    call_price, delta = black_scholes_call(S0, K, T, r, sigma)
    print(f"\nAt t=0:")
    print(f"Call Price: {call_price:.2f}")
    print(f"Delta: {delta:.2f}")

    # Plot stock price path
    path.plot(title="Simulated Stock Price Path")
    plt.xlabel("Time (Years)")
    plt.ylabel("Stock Price")
    plt.grid(True)
    plt.show()

    # Simulate delta hedging
    portfolio, deltas = simulate_delta_hedging(path, K, r, sigma)

    # Plot portfolio value
    portfolio.plot(title="Delta-Hedged Portfolio Value Over Time")
    plt.axhline(0, color='gray', linestyle='--')
    plt.xlabel("Time (Years)")
    plt.ylabel("Portfolio P&L")
    plt.grid(True)
    plt.show()

    # Plot delta values over time
    deltas.plot(title="Delta Over Time")
    plt.xlabel("Time (Years)")
    plt.ylabel("Delta")
    plt.grid(True)
    plt.show()