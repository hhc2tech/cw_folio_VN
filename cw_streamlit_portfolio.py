import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from cw_portfolio import compute_metrics
import os

st.title("Top Covered Warrants Portfolio Analysis")

uploaded = st.file_uploader("Upload portfolio CSV file", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("top10_portfolio.csv")

st.subheader("Raw Portfolio Data")
st.dataframe(df)

summary_df = compute_metrics(df)
top_n = st.slider("Select number of top candidates to review", 1, 10, 5)
top_stocks = summary_df.head(top_n)

st.subheader("📊 Portfolio Metrics")
st.dataframe(summary_df)

st.markdown("### 🔍 Top Potential CW Candidates")
for i in range(len(top_stocks)):
    row = top_stocks.iloc[i]
    if all(k in row for k in ['Ticker', 'Score', 'Avg_Return', 'Volatility', 'Sharpe_Ratio', 'Correlation']):
        st.markdown(
            f"**{row['Ticker']}**: "
            f"Score = {row['Score']:.4f} | "
            f"Return = {row['Avg_Return']:.2%} | "
            f"Risk ≈ {row['Volatility']:.2f} | "
            f"Sharpe ≈ {row['Sharpe_Ratio']:.2f} | "
            f"Corr ≈ {row['Correlation']:.2f}"
        )

# Sharpe Ratio
if st.button("📈 Analyze Sharpe Ratio"):
    st.subheader("Sharpe Ratio by Ticker (Filtered)")
    filtered_df = summary_df.dropna(subset=["Sharpe_Ratio", "Ticker"])
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_df, x='Sharpe_Ratio', y='Ticker', palette='coolwarm', ax=ax)
        ax.set_title("Sharpe Ratio by Ticker")
        st.pyplot(fig)
        if st.checkbox("📥 Export Sharpe Ratio Table"):
            csv_data = filtered_df[['Ticker', 'Sharpe_Ratio']].to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv_data, "sharpe_ratios.csv", "text/csv")
    else:
        st.warning("⚠️ No valid Sharpe Ratio data to display.")

# (Remaining parts unchanged and already working fine)
