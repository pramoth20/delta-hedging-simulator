#  Delta-Hedging-Simulator

**Delta Hedging Simulator**

This project implements a Delta Hedging simulation using historical price data for a listed security (e.g., AAPL) and models the P&L of a dynamically hedged options portfolio over time. It applies quantitative finance concepts like the Black-Scholes model, Greeks, and discrete rebalancing under realistic conditions (e.g., transaction costs, finite hedging frequency).

---

##  Core Concepts

- **Delta Hedging**: A strategy that neutralizes directional risk by taking offsetting positions in the underlying asset and its derivative (option), based on the option’s delta (∂Price/∂Underlying).
- **Black-Scholes Pricing**: A closed-form formula for pricing European options under the assumptions of log-normal returns, constant volatility, and continuous trading.
- **Historical Volatility Estimation**: Realized volatility is estimated from log returns of adjusted close prices and annualized via √252 scaling.
- **Path-Dependent P&L**: The hedging error evolves based on rebalancing frequency and timing relative to price path curvature (gamma exposure).

---

##  Features

-  **Real Data Simulation**: Pulls historical stock prices using `yfinance`, normalizes time to `[0, 1]`.
-  **Delta Rebalancing**: Executes discrete hedging (e.g., every 5 steps), simulating practical rebalancing.
-  **Transaction Costs**: Models proportional costs (default: 0.1%) per trade to mimic realistic execution friction.
-  **Volatility Estimation**: Computes annualized historical volatility from daily log returns.
-  **Greeks Tracking**: Logs delta values at each time step and visualizes their progression.
-  **Interactive Plots**:
  - Normalized asset price path
  - Delta over time
  - Hedged portfolio P&L trajectory

---

##  Example Output

- **Figure**: Delta-Hedged Portfolio Value Over Time  
- **Figure**: Delta Evolution Across Time

---

## ⚙ How It Works

```python
# Load historical price data (auto-adjusted)
data = yf.download("AAPL", start="2024-01-01", end="2024-12-31", auto_adjust=True)

# Estimate annualized historical volatility
sigma = np.std(np.log(data['Close'] / data['Close'].shift(1))) * np.sqrt(252)

# Normalize price path to [0, 1] time and simulate
path = normalize_price_series(data['Close'])
portfolio, deltas = simulate_delta_hedging(path, K=S0, r=0.0443, sigma=sigma)
```

---

##  Black-Scholes Pricing Model

The **Black-Scholes formula** calculates the fair value of a European call option:

$begin:math:display$
C = S \\cdot N(d_1) - K \\cdot e^{-rT} \\cdot N(d_2)
$end:math:display$

Where:

- $begin:math:text$ C $end:math:text$ = Call option price  
- $begin:math:text$ S $end:math:text$ = Current stock price  
- $begin:math:text$ K $end:math:text$ = Strike price  
- $begin:math:text$ T $end:math:text$ = Time to maturity (in years)  
- $begin:math:text$ r $end:math:text$ = Risk-free interest rate  
- $begin:math:text$ \\sigma $end:math:text$ = Volatility of the underlying asset  
- $begin:math:text$ N(d) $end:math:text$ = Cumulative distribution function of the standard normal distribution  

$begin:math:display$
d_1 = \\frac{\\ln(S / K) + (r + \\frac{1}{2}\\sigma^2)T}{\\sigma \\sqrt{T}}, \\quad
d_2 = d_1 - \\sigma \\sqrt{T}
$end:math:display$

**Delta**, the sensitivity of the option price to the stock price, is simply:

$begin:math:display$
\\Delta = N(d_1)
$end:math:display$

Delta increases toward 1.0 as the option becomes deep in-the-money near expiration.

---

##  Future Improvements

- [ ] Incorporate **Gamma** risk and higher-order Greeks
- [ ] Add stochastic volatility models like **GARCH** or **SABR**
- [ ] Expand to **multi-asset** delta-neutral portfolios
- [ ] Backtest strategies across rolling windows and **cross-asset calibration**

---

##  References

- Hull, J. (2022). *Options, Futures, and Other Derivatives*  
- Black, F. & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities*  
- Wilmott, P. (2006). *Paul Wilmott Introduces Quantitative Finance*

---

##  Requirements

```bash
pip install numpy pandas matplotlib yfinance scipy
```

---

##  License

MIT License. Fork, contribute, and build on it!

 License

MIT License. Feel free to fork, extend, and contribute!

