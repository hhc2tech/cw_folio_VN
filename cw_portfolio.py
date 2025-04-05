import pandas as pd
import numpy as np

def compute_metrics(df):
    summary = []
    tickers = df['Ticker'].unique()

    for ticker in tickers:
        subset = df[df['Ticker'] == ticker]
        stock_prices = subset['Stock_Price'].values
        cw_prices = subset['CW_Market_Price'].values

        avg_return = (stock_prices[-1] - stock_prices[0]) / stock_prices[0]
        volatility = np.std(np.diff(stock_prices))  # simple proxy for risk
        cw_change = (cw_prices[-1] - cw_prices[0]) / cw_prices[0]
        stability = -np.std(np.diff(stock_prices))  # lower std = more stable

        score = avg_return * 0.4 + cw_change * 0.3 + stability * 0.3

        summary.append({
            "Ticker": ticker,
            "Avg_Return": avg_return,
            "CW_Change": cw_change,
            "Volatility": volatility,
            "Stability": stability,
            "Score": score
        })

    df_summary = pd.DataFrame(summary).sort_values(by="Score", ascending=False).reset_index(drop=True)
    return df_summary