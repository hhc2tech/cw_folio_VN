import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from cw_portfolio import compute_metrics
from fpdf import FPDF
import tempfile

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

# PDF Report Export using temp file
if st.checkbox("📝 Generate PDF Report"):
    pdf_filename = st.text_input("Enter PDF filename (no extension)", value="cw_portfolio_report")
    if st.button("📄 Create PDF Report"):
        try:
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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                pdf.output(tmpfile.name)
                tmpfile_path = tmpfile.name
            with open(tmpfile_path, "rb") as f:
                st.download_button("📥 Download PDF", data=f, file_name=f"{pdf_filename}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"PDF generation failed: {e}")
