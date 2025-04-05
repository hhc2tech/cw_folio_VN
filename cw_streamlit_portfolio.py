import streamlit as st
import pandas as pd
from cw_portfolio import compute_metrics

st.title("Top Covered Warrants Portfolio Analysis")

uploaded = st.file_uploader("Upload portfolio CSV file", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("top10_portfolio.csv")  # default

st.subheader("Raw Portfolio Data")
st.dataframe(df)

# Compute and show metrics
st.subheader("📊 Computed Portfolio Metrics")
summary_df = compute_metrics(df)
st.dataframe(summary_df.style.highlight_max(axis=0, subset=["Score"], color="lightgreen"))

top_n = st.slider("Select number of top candidates to review", 1, 10, 5)
top_stocks = summary_df.head(top_n)

st.markdown("### 🔍 Top Potential CW Candidates")
for i, row in top_stocks.iterrows():
    st.markdown(f"**{row['Ticker']}**: Score = {row['Score']:.4f} | Return = {row['Avg_Return']:.2%} | Risk ≈ {row['Volatility']:.2f}")

# Optional: Download summary
csv = summary_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Analysis CSV", csv, "portfolio_analysis.csv", "text/csv")