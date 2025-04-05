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
    st.subheader("Sharpe Ratio by Ticker")
    if 'Sharpe_Ratio' in summary_df.columns and 'Ticker' in summary_df.columns:
        filtered_df = summary_df[['Sharpe_Ratio', 'Ticker']].dropna()
        if not filtered_df.empty:
            fig, ax = plt.subplots()
            sns.barplot(data=filtered_df, x='Sharpe_Ratio', y='Ticker', palette='coolwarm', ax=ax)
            ax.set_title("Sharpe Ratio by Ticker")
            st.pyplot(fig)
            if st.checkbox("📥 Export Sharpe Ratio Table"):
                csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv_data, "sharpe_ratios.csv", "text/csv")
        else:
            st.warning("⚠️ No valid Sharpe Ratio data to display.")
    else:
        st.warning("⚠️ 'Sharpe_Ratio' or 'Ticker' column missing.")

# CW P&L
if st.button("💰 Simulate CW P&L Over Time"):
    pnl_data = []
    if 'Ticker' in df.columns and 'CW_Market_Price' in df.columns and 'Day' in df.columns:
        for ticker in df['Ticker'].unique():
            subset = df[df['Ticker'] == ticker].copy()
            subset['CW_PnL'] = subset['CW_Market_Price'].diff()
            pnl_data.append(subset[['Ticker', 'Day', 'CW_PnL']])
        df_pnl = pd.concat(pnl_data)
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=df_pnl, x='Day', y='CW_PnL', hue='Ticker', marker='o', ax=ax)
        ax.set_title("CW Daily P&L Simulation")
        st.pyplot(fig)
        if st.checkbox("📥 Export CW P&L Table"):
            st.download_button("Download CSV", df_pnl.to_csv(index=False).encode('utf-8'), "cw_pnl_over_time.csv", "text/csv")
    else:
        st.warning("⚠️ Missing required columns for P&L simulation.")

# Correlation
if st.button("🔗 Correlation Between Stock and CW"):
    st.subheader("Correlation Between Stock Price and CW Price")
    corr_data = []
    if 'Ticker' in df.columns and 'Stock_Price' in df.columns and 'CW_Market_Price' in df.columns:
        for ticker in df['Ticker'].unique():
            sub = df[df['Ticker'] == ticker]
            corr = sub['Stock_Price'].corr(sub['CW_Market_Price'])
            corr_data.append({'Ticker': ticker, 'Correlation': corr})
        df_corr = pd.DataFrame(corr_data).sort_values(by='Correlation', ascending=False)
        fig, ax = plt.subplots()
        sns.barplot(data=df_corr, x='Correlation', y='Ticker', palette='vlag', ax=ax)
        ax.set_title("Correlation: Stock Price vs CW Market Price")
        st.pyplot(fig)
        if st.checkbox("📥 Export Correlation Table"):
            st.download_button("Download CSV", df_corr.to_csv(index=False).encode('utf-8'), "correlations.csv", "text/csv")
    else:
        st.warning("⚠️ Missing columns for correlation analysis.")

# PDF generation
if st.checkbox("📝 Generate PDF Report"):
    try:
        from fpdf import FPDF
        pdf_filename = st.text_input("Enter PDF filename (no extension)", value="cw_portfolio_report")
        if st.button("📄 Create PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="CW Portfolio Analysis Report", ln=True, align='C')
            pdf.ln(10)
            for _, row in summary_df.iterrows():
                if all(k in row for k in ['Ticker', 'Score', 'Avg_Return', 'Volatility', 'Sharpe_Ratio', 'Correlation']):
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(0, 8,
                        f"{row['Ticker']}: Return = {row['Avg_Return']:.2%}, "
                        f"Risk = {row['Volatility']:.2f}, "
                        f"Sharpe = {row['Sharpe_Ratio']:.2f}, "
                        f"Corr = {row['Correlation']:.2f}, "
                        f"Score = {row['Score']:.4f}"
                    )
            final_path = f"/mnt/data/{pdf_filename}.pdf"
            pdf.output(final_path)
            with open(final_path, "rb") as f:
                st.download_button("📥 Download PDF", data=f, file_name=f"{pdf_filename}.pdf", mime="application/pdf")
    except ImportError:
        st.warning("⚠️ FPDF not installed. Run `pip install fpdf` to enable PDF export.")
