import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from cw_portfolio import compute_metrics
from fpdf import FPDF
import tempfile

st.set_page_config(layout="wide")
st.title("📊 Top Covered Warrants Portfolio Analysis")

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
    try:
        st.markdown(
            f"**{row['Ticker']}**: "
            f"Score = {row['Score']:.4f} | "
            f"Return = {row['Avg_Return']:.2%} | "
            f"Risk ≈ {row['Volatility']:.2f} | "
            f"Sharpe ≈ {row['Sharpe_Ratio']:.2f} | "
            f"Corr ≈ {row['Correlation']:.2f}"
        )
    except:
        continue

# Sharpe Ratio Analysis
if st.button("📈 Analyze Sharpe Ratio"):
    st.subheader("Sharpe Ratio by Ticker")
    if 'Sharpe_Ratio' in summary_df.columns and 'Ticker' in summary_df.columns:
        filtered_df = summary_df[['Sharpe_Ratio', 'Ticker']].dropna()
        if not filtered_df.empty:
            fig, ax = plt.subplots()
            sns.barplot(data=filtered_df, x='Sharpe_Ratio', y='Ticker', palette='coolwarm', ax=ax)
            ax.set_title("Sharpe Ratio by Ticker")
            st.pyplot(fig)
            st.download_button("📥 Download Sharpe Ratios CSV", filtered_df.to_csv(index=False).encode('utf-8'), "sharpe_ratios.csv", "text/csv")
        else:
            st.warning("⚠️ No valid Sharpe Ratio data to display.")

# P&L Simulation
if st.button("💰 Simulate CW P&L Over Time"):
    if all(col in df.columns for col in ['Ticker', 'CW_Market_Price', 'Day']):
        pnl_data = []
        for ticker in df['Ticker'].unique():
            sub = df[df['Ticker'] == ticker].copy()
            sub['CW_PnL'] = sub['CW_Market_Price'].diff()
            pnl_data.append(sub[['Ticker', 'Day', 'CW_PnL']])
        df_pnl = pd.concat(pnl_data)
        fig, ax = plt.subplots()
        sns.lineplot(data=df_pnl, x='Day', y='CW_PnL', hue='Ticker', marker='o', ax=ax)
        ax.set_title("CW Daily P&L Simulation")
        st.pyplot(fig)
        st.download_button("📥 Download CW P&L CSV", df_pnl.to_csv(index=False).encode('utf-8'), "cw_pnl_over_time.csv", "text/csv")
    else:
        st.warning("⚠️ Required columns missing for CW P&L.")

# Correlation
if st.button("🔗 Correlation Between Stock and CW"):
    if all(col in df.columns for col in ['Ticker', 'Stock_Price', 'CW_Market_Price']):
        corr_data = []
        for ticker in df['Ticker'].unique():
            sub = df[df['Ticker'] == ticker]
            corr = sub['Stock_Price'].corr(sub['CW_Market_Price'])
            corr_data.append({'Ticker': ticker, 'Correlation': corr})
        df_corr = pd.DataFrame(corr_data).sort_values(by='Correlation', ascending=False)
        fig, ax = plt.subplots()
        sns.barplot(data=df_corr, x='Correlation', y='Ticker', palette='vlag', ax=ax)
        ax.set_title("Correlation: Stock Price vs CW Market Price")
        st.pyplot(fig)
        st.download_button("📥 Download Correlation CSV", df_corr.to_csv(index=False).encode('utf-8'), "correlations.csv", "text/csv")
    else:
        st.warning("⚠️ Required columns missing for correlation analysis.")

# PDF Report Export
st.markdown("### 📝 Export Full Report")
if st.checkbox("📄 Generate PDF Report"):
    pdf_filename = st.text_input("Enter PDF filename (no extension)", value="cw_portfolio_report")
    if st.button("🧾 Create PDF Report"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "CW Portfolio Analysis Report", ln=True, align='C')
            pdf.set_font("Arial", "", 11)
            pdf.ln(5)
            for _, row in summary_df.iterrows():
                try:
                    line = (
                        f"{row['Ticker']}: "
                        f"Return = {row['Avg_Return']:.2%}, "
                        f"Risk = {row['Volatility']:.2f}, "
                        f"Sharpe = {row['Sharpe_Ratio']:.2f}, "
                        f"Corr = {row['Correlation']:.2f}, "
                        f"Score = {row['Score']:.4f}"
                    )
                    pdf.multi_cell(0, 8, line)
                except:
                    continue
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                pdf.output(tmpfile.name)
                tmpfile_path = tmpfile.name
            with open(tmpfile_path, "rb") as f:
                st.download_button("📥 Download PDF", data=f, file_name=f"{pdf_filename}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"PDF generation failed: {e}")
