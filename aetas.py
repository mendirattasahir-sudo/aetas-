import yfinance as yf
from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Aetas", page_icon="●", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .block-container { max-width: 700px; padding-top: 3rem; }
    h1 {
        font-family: Georgia, serif;
        font-size: 36px;
        letter-spacing: 10px;
        text-align: center;
        color: #ffffff;
        margin-bottom: 0;
    }
    .tagline {
        text-align: center;
        font-size: 11px;
        color: #5a5a5a;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 2.5rem;
    }
    .stTextInput input {
        background-color: #0a0a0a;
        border: 0.5px solid #2a2a2a;
        border-radius: 6px;
        color: #e5e5e5;
        font-size: 13px;
    }
    .stButton button {
        background-color: #ffffff;
        border: none;
        border-radius: 6px;
        color: #000000;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 1px;
        padding: 10px 24px;
    }
    .company-name {
        font-family: Georgia, serif;
        font-size: 20px;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 2px;
    }
    .ticker-label {
        font-size: 10px;
        color: #5a5a5a;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    .memo-label {
        font-size: 10px;
        color: #4a4a4a;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-align: center;
        margin: 2rem 0 1.25rem 0;
    }
    .memo-section {
        margin-bottom: 18px;
        padding-left: 14px;
        border-left: 1px solid #2a2a2a;
    }
    .memo-title {
        font-size: 11px;
        font-weight: 500;
        color: #ffffff;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .memo-text {
        font-size: 13px;
        color: #8a8a8a;
        line-height: 1.7;
    }
    .footer-text {
        font-size: 9px;
        color: #3a3a3a;
        letter-spacing: 2px;
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 0.5px solid #1a1a1a;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>AETAS</h1>", unsafe_allow_html=True)
st.markdown('<div class="tagline">AI Credit Underwriting · NSE Listed Companies</div>', unsafe_allow_html=True)

companies = {
    "TCS": "TCS.NS",
    "Reliance Industries": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "State Bank of India": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Wipro": "WIPRO.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Larsen & Toubro": "LT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Tata Steel": "TATASTEEL.NS",
"Adani Enterprises": "ADANIENT.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    "Bharat Petroleum": "BPCL.NS",
    "Britannia": "BRITANNIA.NS",
    "Cipla": "CIPLA.NS",
    "Coal India": "COALINDIA.NS",
    "Divi's Laboratories": "DIVISLAB.NS",
    "Dr Reddy's Labs": "DRREDDY.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Grasim Industries": "GRASIM.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Hindalco": "HINDALCO.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Nestle India": "NESTLEIND.NS",
    "NTPC": "NTPC.NS",
    "ONGC": "ONGC.NS",
    "Power Grid": "POWERGRID.NS",
    "Tata Consumer Products": "TATACONSUM.NS",
    "Tech Mahindra": "TECHM.NS",
    "Titan Company": "TITAN.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Zomato": "ZOMATO.NS",
    "Paytm": "PAYTM.NS",
    "Nykaa": "NYKAA.NS",
    "Vedanta": "VEDL.NS",
    "Godrej Consumer": "GODREJCP.NS",
    "Pidilite Industries": "PIDILITIND.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS",
    "Shree Cement": "SHREECEM.NS",
    "Siemens": "SIEMENS.NS",
    "ABB India": "ABB.NS",
    "DLF": "DLF.NS",
    "Indian Oil": "IOC.NS",
    "GAIL": "GAIL.NS",}

selected_company = st.selectbox("", options=[""] + list(companies.keys()), format_func=lambda x: "Search for a company — e.g. HDFC Bank" if x == "" else x)
ticker = companies.get(selected_company, "")
generate = st.button("Generate")

if generate:
    if not ticker:
        st.warning("Please enter a ticker symbol.")
    else:
        with st.spinner("Pulling financials and generating memo..."):
            try:
                stock = yf.Ticker(ticker)
                info = stock.info

                company = info.get('longName', 'N/A')
                sector = info.get('sector', 'N/A')
                revenue = info.get('totalRevenue', 0)
                ebitda = info.get('ebitda', 0)
                total_debt = info.get('totalDebt', 0)
                fcf = info.get('freeCashflow', 0)

                if not revenue:
                    st.error("Data not available for this ticker. Try a different NSE-listed company.")
                else:
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

                    st.markdown(f'<div class="company-name">{company}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="ticker-label">{ticker.upper()} · {sector}</div>', unsafe_allow_html=True)

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Revenue", f"₹{round(revenue/1e7):,} Cr")
                    col2.metric("EBITDA", f"₹{round(ebitda/1e7):,} Cr")
                    col3.metric("Leverage", f"{leverage}x")
                    col4.metric("FCF Cover", f"{fcf_coverage}x")

                    st.write("")
                    if leverage < 3:
                        st.success("LOW LEVERAGE — STRONG CREDIT PROFILE")
                    elif leverage < 5:
                        st.warning("MODERATE LEVERAGE — MONITOR CLOSELY")
                    else:
                        st.error("HIGH LEVERAGE — ELEVATED CREDIT RISK")

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are a senior credit analyst at a private credit fund. Write concise, professional credit memos with three clearly labeled sections: Investment Thesis, Key Risks, Recommendation. Each section should be 2-3 sentences max."},
                            {"role": "user", "content": f"Write a credit memo for the following company.\n\n{financials_summary}"}
                        ]
                    )

                    st.markdown('<div class="memo-label">Credit Memo</div>', unsafe_allow_html=True)
                    st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error("Could not retrieve data for this ticker. Please check the symbol and try again.")

st.markdown('<div class="footer-text">Aetas · Built by Sahir Mendiratta</div>', unsafe_allow_html=True)