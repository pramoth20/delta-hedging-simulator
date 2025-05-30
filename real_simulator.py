import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import yfinance as yf

# --- Load Real Historical Stock Data ---
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    if data.empty:
        raise ValueError(f"No price data found for {ticker} between {start_date} and {end_date}")
    return data['Close']

# --- Estimate Annualized Volatility ---
def estimate_volatility(price_series):
    log_returns = np.log(price_series / price_series.shift(1)).dropna()
    return log_returns.std() * np.sqrt(252)

# --- Normalize Prices and Time ---
def normalize_price_series(price_series):
    base = float(price_series.iloc[0])
    normalized = price_series / base * 100
    normalized.index = np.linspace(0, 1, len(normalized))  # normalize time from 0 to 1
    return normalized

# --- Black-Scholes Formula ---
def black_scholes_call(S, K, T, r, sigma):
    S, K, T, r, sigma = map(float, [S, K, T, r, sigma])
    if T <= 0:
        return max(S - K, 0), 1.0 if S > K else 0.0
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
        S = float(path.iloc[i])
        t = i * dt
        T_remaining = 1 - t
        option_price, delta = black_scholes_call(S, K, T_remaining, r, sigma)
        deltas.append(delta)

        if i == 0:
            trade_amount = delta * S
            cost = abs(trade_amount) * transaction_cost
            cash = option_price - trade_amount - cost
            shares_held = delta
        elif i % hedge_every == 0:
            new_shares = delta
            trade_amount = (new_shares - shares_held) * S
            cost = abs(trade_amount) * transaction_cost
            cash -= trade_amount + cost
            shares_held = new_shares

        value = shares_held * S + cash - option_price
        portfolio_value.append(value)

        print(f"Step {i} | S={S:.2f}, T_remain={T_remaining:.3f}, sigma={sigma:.3f} → Call: {option_price:.2f}, Delta: {delta:.2f}")

    portfolio_series = pd.to_numeric(pd.Series(portfolio_value, index=path.index), errors='coerce')
    delta_series = pd.Series(deltas, index=path.index)
    return portfolio_series, delta_series

# --- MAIN ---
if __name__ == "__main__":
    ticker = 'AAPL'
    start_date = '2024-01-01'
    end_date = '2024-12-31'
    r = 0.0443  # Risk-free rate

    raw_prices = get_stock_data(ticker, start_date, end_date)
    print("Data preview:\n", raw_prices.head())  # 🛠 debug
    sigma = float(estimate_volatility(raw_prices))
    path = normalize_price_series(raw_prices)
    S0 = float(path.iloc[0])
    K = S0

    call_price, delta = black_scholes_call(S0, K, 1, r, sigma)
    print(f"\n{ticker} Real Data")
    print(f"Call Price at t=0: {call_price:.2f}")
    print(f"Delta at t=0: {delta:.2f}")
    print(f"Estimated Annual Volatility: {float(sigma):.2%}")

    # Plot price path
    path.plot(title=f"{ticker} Normalized Stock Price Path")
    plt.xlabel("Time (Years)")
    plt.ylabel("Stock Price (Normalized)")
    plt.grid(True)
    plt.show()

    # Run delta hedging
    portfolio, deltas = simulate_delta_hedging(path, K, r, sigma)

    # Plot P&L
    portfolio.plot(title="Delta-Hedged Portfolio Value Over Time")
    plt.axhline(0, color='gray', linestyle='--')
    plt.xlabel("Time (Years)")
    plt.ylabel("Portfolio P&L")
    plt.grid(True)
    plt.show()

    # Plot Delta
    deltas.plot(title="Delta Over Time")
    plt.xlabel("Time (Years)")
    plt.ylabel("Delta")
    plt.grid(True)
    plt.show()