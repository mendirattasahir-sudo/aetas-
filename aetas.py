import yfinance as yf
from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("Aetas")
st.subheader("AI Credit Underwriting Tool")
st.write("Enter any NSE-listed company ticker to generate an instant credit memo.")

ticker = st.text_input("NSE Ticker (e.g. TCS.NS, RELIANCE.NS, HDFCBANK.NS)")

if st.button("Generate Credit Memo"):
    with st.spinner("Pulling financials and generating memo..."):
        stock = yf.Ticker(ticker)
        info = stock.info

        company = info.get('longName', 'N/A')
        revenue = info.get('totalRevenue', 0)
        ebitda = info.get('ebitda', 0)
        total_debt = info.get('totalDebt', 0)
        fcf = info.get('freeCashflow', 0)

        leverage = round(total_debt / ebitda, 2) if ebitda else 0
        fcf_coverage = round(fcf / total_debt, 2) if total_debt else 0

        financials_summary = f"""
Company: {company}
Revenue: ₹{round(revenue/1e7):,} Cr
EBITDA: ₹{round(ebitda/1e7):,} Cr
Total Debt: ₹{round(total_debt/1e7):,} Cr
Free Cash Flow: ₹{round(fcf/1e7):,} Cr
Debt/EBITDA Leverage: {leverage}x
FCF Coverage: {fcf_coverage}x
"""

        st.subheader(f"Credit Snapshot — {company}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Leverage", f"{leverage}x")
        col2.metric("FCF Coverage", f"{fcf_coverage}x")
        col3.metric("Total Debt", f"₹{round(total_debt/1e7):,} Cr")

        if leverage < 3:
            st.success("Risk Flag: LOW LEVERAGE ✓")
        elif leverage < 5:
            st.warning("Risk Flag: MODERATE LEVERAGE ⚠️")
        else:
            st.error("Risk Flag: HIGH LEVERAGE ✗")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a senior credit analyst at a private credit fund. Write concise, professional credit memos."},
                {"role": "user", "content": f"Write a short credit memo for the following company. Include: 1) Investment thesis 2) Key risks 3) Loan recommendation.\n\n{financials_summary}"}
            ]
        )

        st.subheader("Credit Memo")
        st.write(response.choices[0].message.content)