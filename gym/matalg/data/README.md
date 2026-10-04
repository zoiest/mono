# Multivariate Financial Asset Returns Dataset

This dataset contains $N = 250$ business days of simulated daily asset returns across $p = 6$ major exchange-traded funds (ETFs) designed for practical matrix algebra exercises.

## Asset Universe

| Ticker | Asset Class / Sector | Economic Role | Expected Annualized Volatility |
|:-------|:---------------------|:--------------|:------------------------------:|
| **SPY** | US Large-Cap Equities (S&P 500) | Broad Market Benchmark | 16% |
| **QQQ** | US Tech & Growth (Nasdaq 100) | High Beta / Tech Growth | 22% |
| **GLD** | Physical Gold Commodity | Inflation & Crisis Hedge | 14% |
| **XLE** | Energy Sector Equities | Cyclical Commodity Equities | 28% |
| **TLT** | 20+ Year US Treasury Bonds | Fixed Income Duration / Flight-to-Safety | 15% |
| **VNQ** | US Real Estate Investment Trusts | Yield / Real Asset Exposure | 20% |

## Properties for Matrix Computing

1. **Covariance Matrix Dimension:** $6 \times 6$, strictly positive definite.
2. **Correlation Dynamics:**
   - $\text{Corr}(\text{SPY}, \text{QQQ}) \approx 0.88$ (strong equity co-movement).
   - $\text{Corr}(\text{SPY}, \text{TLT}) \approx -0.38$ (flight-to-safety duration hedge).
   - $\text{Corr}(\text{GLD}, \text{SPY}) \approx 0.12$ (diversifying safe haven).
3. **Condition Number:** $\kappa(S) \approx 25$ to $40$ (moderately conditioned, ideal for demonstrating why QR and Cholesky are superior to naive inversion).
4. **Injected Market Shock:**
   - **Day 180** contains an exogenous shock event simulating a severe market dislocation (simultaneous drop in equities/energy accompanied by flight to Treasuries and Gold), providing a benchmark for Mahalanobis anomaly detection and Hotelling's $T^2$ test.
