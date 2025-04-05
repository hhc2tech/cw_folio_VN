import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from cw_portfolio import compute_metrics

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

# Fix: Ensure Sharpe_Ratio & Ticker exist
if "Sharpe_Ratio" not in summary_df.columns:
    summary_df["Sharpe_Ratio"] = summary_df["Avg_Return"] / summary_df["Volatility"].replace(0, 1)
if "Ticker" not in summary_df.columns and "ticker" in summary_df.columns:
    summary_df["Ticker"] = summary_df["ticker"]

# Sharpe Ratio
if st.button("📈 Analyze Sharpe Ratio"):
    st.subheader("Sharpe Ratio by Ticker")
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
                try:
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(0, 8,
                        f"{row['Ticker']}: Return = {row['Avg_Return']:.2%}, "
                        f"Risk = {row['Volatility']:.2f}, "
                        f"Sharpe = {row['Sharpe_Ratio']:.2f}, "
                        f"Corr = {row['Correlation']:.2f}, "
                        f"Score = {row['Score']:.4f}"
                    )
                except:
                    continue
            os.makedirs("/mnt/data", exist_ok=True)
            final_path = f"/mnt/data/{pdf_filename}.pdf"
            pdf.output(final_path)
            with open(final_path, "rb") as f:
                st.download_button("📥 Download PDF", data=f, file_name=f"{pdf_filename}.pdf", mime="application/pdf")
    except ImportError:
        st.warning("⚠️ FPDF not installed. Run `pip install fpdf` to enable PDF export.")
