#!/usr/bin/env python3
"""
Generates a realistic 6-asset multivariate daily returns dataset (250 trading days).
Uses standard library csv and numpy for zero extra dependencies.
"""

import csv
import datetime
import numpy as np
from pathlib import Path

def generate_returns(n_days: int = 250, seed: int = 42):
    np.random.seed(seed)
    assets = ["SPY", "QQQ", "GLD", "XLE", "TLT", "VNQ"]
    p = len(assets)
    
    # Ground truth correlation matrix
    # SPY & QQQ high positive correlation
    # SPY & TLT negative correlation
    # GLD mild positive / hedge
    # XLE cyclical
    corr = np.array([
        # SPY   QQQ   GLD   XLE   TLT   VNQ
        [1.00, 0.88, 0.12, 0.55,-0.38, 0.65],  # SPY
        [0.88, 1.00, 0.08, 0.42,-0.32, 0.58],  # QQQ
        [0.12, 0.08, 1.00, 0.20, 0.25, 0.15],  # GLD
        [0.55, 0.42, 0.20, 1.00,-0.22, 0.48],  # XLE
        [-0.38,-0.32, 0.25,-0.22, 1.00,-0.18],  # TLT
        [0.65, 0.58, 0.15, 0.48,-0.18, 1.00],  # VNQ
    ])
    
    # Ensure positive definiteness
    evals, evecs = np.linalg.eigh(corr)
    evals = np.maximum(evals, 1e-4)
    corr = evecs @ np.diag(evals) @ evecs.T
    d = np.sqrt(np.diag(corr))
    corr = corr / np.outer(d, d)
    
    # Annualized volatilities -> daily volatilities (assuming 252 trading days)
    ann_vols = np.array([0.16, 0.22, 0.14, 0.28, 0.15, 0.20])
    daily_vols = ann_vols / np.sqrt(252)
    
    # Covariance matrix: Sigma = D * corr * D
    D = np.diag(daily_vols)
    cov = D @ corr @ D
    
    # Daily expected returns
    ann_ret = np.array([0.10, 0.14, 0.06, 0.08, 0.03, 0.07])
    daily_mean = ann_ret / 252.0
    
    # Generate random multivariate normal draws using Cholesky factorization
    L = np.linalg.cholesky(cov)
    Z = np.random.randn(n_days, p)
    returns = daily_mean + Z @ L.T
    
    # Inject a known shock/anomaly on Day 180 (market crash + flight to treasuries/gold)
    returns[180, :] = np.array([-0.042, -0.058, 0.025, -0.065, 0.032, -0.048])
    
    # Generate business dates
    cur = datetime.date(2025, 1, 2)
    dates = []
    while len(dates) < n_days:
        if cur.weekday() < 5:  # Monday to Friday
            dates.append(cur.strftime("%Y-%m-%d"))
        cur += datetime.timedelta(days=1)
        
    return assets, dates, returns

def main():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    assets, dates, returns = generate_returns()
    csv_path = data_dir / "asset_returns.csv"
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date"] + assets)
        for date, row in zip(dates, returns):
            writer.writerow([date] + [f"{val:.6f}" for val in row])
            
    print(f"Generated {csv_path} with {len(dates)} rows and {len(assets)} assets.")
    print("Assets:", assets)
    print("Sample mean vector:", np.mean(returns, axis=0))
    print("Sample standard deviations:", np.std(returns, axis=0))

if __name__ == "__main__":
    main()
