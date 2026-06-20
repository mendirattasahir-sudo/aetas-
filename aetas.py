import yfinance as yf
from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Aetas", page_icon="●", layout="centered")

st.markdown("""
<style>[data-testid="stMetricValue"] {
        font-size: 16px !important;
    }
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
    .grade-box {
        text-align: center;
        margin: 1.5rem 0;
    }
    .grade-text {
        font-family: Georgia, serif;
        font-size: 40px;
        font-weight: 500;
        color: #ffffff;
        letter-spacing: 4px;
    }
    .grade-label {
        font-size: 10px;
        color: #5a5a5a;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .vs-divider {
        text-align: center;
        font-family: Georgia, serif;
        font-size: 14px;
        color: #5a5a5a;
        letter-spacing: 4px;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>AETAS</h1>", unsafe_allow_html=True)
st.markdown('<div class="tagline">AI Credit Underwriting · NSE & BSE Listed Companies</div>', unsafe_allow_html=True)

companies = {
    "TCS": {"NSE": "TCS.NS", "BSE": "TCS.BO"},
    "Reliance Industries": {"NSE": "RELIANCE.NS", "BSE": "RELIANCE.BO"},
    "HDFC Bank": {"NSE": "HDFCBANK.NS", "BSE": "HDFCBANK.BO"},
    "Infosys": {"NSE": "INFY.NS", "BSE": "INFY.BO"},
    "ICICI Bank": {"NSE": "ICICIBANK.NS", "BSE": "ICICIBANK.BO"},
    "Hindustan Unilever": {"NSE": "HINDUNILVR.NS", "BSE": "HINDUNILVR.BO"},
    "ITC": {"NSE": "ITC.NS", "BSE": "ITC.BO"},
    "State Bank of India": {"NSE": "SBIN.NS", "BSE": "SBIN.BO"},
    "Bharti Airtel": {"NSE": "BHARTIARTL.NS", "BSE": "BHARTIARTL.BO"},
    "Tata Motors": {"NSE": "TATAMOTORS.NS", "BSE": "TATAMOTORS.BO"},
    "Wipro": {"NSE": "WIPRO.NS", "BSE": "WIPRO.BO"},
    "Asian Paints": {"NSE": "ASIANPAINT.NS", "BSE": "ASIANPAINT.BO"},
    "Maruti Suzuki": {"NSE": "MARUTI.NS", "BSE": "MARUTI.BO"},
    "Larsen & Toubro": {"NSE": "LT.NS", "BSE": "LT.BO"},
    "Axis Bank": {"NSE": "AXISBANK.NS", "BSE": "AXISBANK.BO"},
    "Bajaj Finance": {"NSE": "BAJFINANCE.NS", "BSE": "BAJFINANCE.BO"},
    "Kotak Mahindra Bank": {"NSE": "KOTAKBANK.NS", "BSE": "KOTAKBANK.BO"},
    "HCL Technologies": {"NSE": "HCLTECH.NS", "BSE": "HCLTECH.BO"},
    "Sun Pharma": {"NSE": "SUNPHARMA.NS", "BSE": "SUNPHARMA.BO"},
    "Tata Steel": {"NSE": "TATASTEEL.NS", "BSE": "TATASTEEL.BO"},
    "Adani Enterprises": {"NSE": "ADANIENT.NS", "BSE": "ADANIENT.BO"},
    "Adani Ports": {"NSE": "ADANIPORTS.NS", "BSE": "ADANIPORTS.BO"},
    "Bajaj Auto": {"NSE": "BAJAJ-AUTO.NS", "BSE": "BAJAJ-AUTO.BO"},
    "Bajaj Finserv": {"NSE": "BAJAJFINSV.NS", "BSE": "BAJAJFINSV.BO"},
    "Bharat Petroleum": {"NSE": "BPCL.NS", "BSE": "BPCL.BO"},
    "Britannia": {"NSE": "BRITANNIA.NS", "BSE": "BRITANNIA.BO"},
    "Cipla": {"NSE": "CIPLA.NS", "BSE": "CIPLA.BO"},
    "Coal India": {"NSE": "COALINDIA.NS", "BSE": "COALINDIA.BO"},
    "Divi's Laboratories": {"NSE": "DIVISLAB.NS", "BSE": "DIVISLAB.BO"},
    "Dr Reddy's Labs": {"NSE": "DRREDDY.NS", "BSE": "DRREDDY.BO"},
    "Eicher Motors": {"NSE": "EICHERMOT.NS", "BSE": "EICHERMOT.BO"},
    "Grasim Industries": {"NSE": "GRASIM.NS", "BSE": "GRASIM.BO"},
    "HDFC Life": {"NSE": "HDFCLIFE.NS", "BSE": "HDFCLIFE.BO"},
    "Hero MotoCorp": {"NSE": "HEROMOTOCO.NS", "BSE": "HEROMOTOCO.BO"},
    "Hindalco": {"NSE": "HINDALCO.NS", "BSE": "HINDALCO.BO"},
    "IndusInd Bank": {"NSE": "INDUSINDBK.NS", "BSE": "INDUSINDBK.BO"},
    "JSW Steel": {"NSE": "JSWSTEEL.NS", "BSE": "JSWSTEEL.BO"},
    "Mahindra & Mahindra": {"NSE": "M&M.NS", "BSE": "M&M.BO"},
    "Nestle India": {"NSE": "NESTLEIND.NS", "BSE": "NESTLEIND.BO"},
    "NTPC": {"NSE": "NTPC.NS", "BSE": "NTPC.BO"},
    "ONGC": {"NSE": "ONGC.NS", "BSE": "ONGC.BO"},
    "Power Grid": {"NSE": "POWERGRID.NS", "BSE": "POWERGRID.BO"},
    "Tata Consumer Products": {"NSE": "TATACONSUM.NS", "BSE": "TATACONSUM.BO"},
    "Tech Mahindra": {"NSE": "TECHM.NS", "BSE": "TECHM.BO"},
    "Titan Company": {"NSE": "TITAN.NS", "BSE": "TITAN.BO"},
    "UltraTech Cement": {"NSE": "ULTRACEMCO.NS", "BSE": "ULTRACEMCO.BO"},
    "Zomato": {"NSE": "ZOMATO.NS", "BSE": "ZOMATO.BO"},
    "Paytm": {"NSE": "PAYTM.NS", "BSE": "PAYTM.BO"},
    "Nykaa": {"NSE": "NYKAA.NS", "BSE": "NYKAA.BO"},
    "Vedanta": {"NSE": "VEDL.NS", "BSE": "VEDL.BO"},
    "Godrej Consumer": {"NSE": "GODREJCP.NS", "BSE": "GODREJCP.BO"},
    "Pidilite Industries": {"NSE": "PIDILITIND.NS", "BSE": "PIDILITIND.BO"},
    "Apollo Hospitals": {"NSE": "APOLLOHOSP.NS", "BSE": "APOLLOHOSP.BO"},
    "Shree Cement": {"NSE": "SHREECEM.NS", "BSE": "SHREECEM.BO"},
    "Siemens": {"NSE": "SIEMENS.NS", "BSE": "SIEMENS.BO"},
    "ABB India": {"NSE": "ABB.NS", "BSE": "ABB.BO"},
    "DLF": {"NSE": "DLF.NS", "BSE": "DLF.BO"},
    "Indian Oil": {"NSE": "IOC.NS", "BSE": "IOC.BO"},
    "GAIL": {"NSE": "GAIL.NS", "BSE": "GAIL.BO"},
}


def analyze_company(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    company = info.get('longName', 'N/A')
    sector = info.get('sector', 'N/A')
    revenue = info.get('totalRevenue', 0)
    ebitda = info.get('ebitda', 0)
    total_debt = info.get('totalDebt', 0)
    fcf = info.get('freeCashflow', 0)
    cash = info.get('totalCash', 0)
    roe = info.get('returnOnEquity', 0)

    try:
        bs = stock.balance_sheet
        current_assets = float(bs.loc['Current Assets'].iloc[0]) if 'Current Assets' in bs.index else 0
        current_liabilities = float(bs.loc['Current Liabilities'].iloc[0]) if 'Current Liabilities' in bs.index else 0
    except Exception:
        current_assets = 0
        current_liabilities = 0

    try:
        inc = stock.income_stmt
        interest_expense = float(inc.loc['Interest Expense'].iloc[0]) if 'Interest Expense' in inc.index else 0
    except Exception:
        interest_expense = 0

    try:
        news = stock.news[:5]
        news_text = "\n".join([f"- {n.get('content', {}).get('title', '')}" for n in news]) if news else "No recent news available."
    except Exception:
        news_text = "No recent news available."

    if not revenue:
        return None

    leverage = round(total_debt / ebitda, 2) if ebitda else 0
    fcf_coverage = round(fcf / total_debt, 2) if total_debt else 0
    net_debt = total_debt - cash
    current_ratio = round(current_assets / current_liabilities, 2) if current_liabilities else 0
    interest_coverage = round(ebitda / abs(interest_expense), 2) if interest_expense else 0
    roe_pct = round(roe * 100, 1) if roe else 0

    score = 0
    if leverage < 2:
        score += 3
    elif leverage < 4:
        score += 2
    elif leverage < 6:
        score += 1

    if fcf_coverage > 2:
        score += 3
    elif fcf_coverage > 1:
        score += 2
    elif fcf_coverage > 0:
        score += 1

    if interest_coverage > 5:
        score += 3
    elif interest_coverage > 2:
        score += 2
    elif interest_coverage > 1:
        score += 1

    if current_ratio > 1.5:
        score += 2
    elif current_ratio > 1:
        score += 1

    if score >= 10:
        grade = "AAA"
    elif score >= 8:
        grade = "AA"
    elif score >= 6:
        grade = "A"
    elif score >= 4:
        grade = "BBB"
    elif score >= 2:
        grade = "BB"
    else:
        grade = "B"

    financials_summary = f"""
Company: {company}
Sector: {sector}
Revenue: Rs {round(revenue/1e7):,} Cr
EBITDA: Rs {round(ebitda/1e7):,} Cr
Total Debt: Rs {round(total_debt/1e7):,} Cr
Free Cash Flow: Rs {round(fcf/1e7):,} Cr
Debt/EBITDA Leverage: {leverage}x
FCF Coverage: {fcf_coverage}x
Interest Coverage: {interest_coverage}x
Current Ratio: {current_ratio}x
ROE: {roe_pct}%

Recent News Headlines:
{news_text}
"""

    return {
        "company": company,
        "sector": sector,
        "ticker": ticker,
        "revenue": revenue,
        "ebitda": ebitda,
        "leverage": leverage,
        "fcf_coverage": fcf_coverage,
        "net_debt": net_debt,
        "current_ratio": current_ratio,
        "interest_coverage": interest_coverage,
        "roe_pct": roe_pct,
        "grade": grade,
        "score": score,
        "news_text": news_text,
        "financials_summary": financials_summary,
    }


def render_metrics(result):
    st.markdown(f'<div class="company-name">{result["company"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-label">{result["ticker"].upper()} - {result["sector"]}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue", f"Rs {round(result['revenue']/1e9, 1)}K Cr")
    col2.metric("EBITDA", f"Rs {round(result['ebitda']/1e9, 1)}K Cr")
    col3.metric("Leverage", f"{result['leverage']}x")
    col4.metric("FCF Cover", f"{result['fcf_coverage']}x")

    col5, col6, col7, col8 = st.columns(4)
    net_debt = result["net_debt"]
    net_debt_label = "Net Cash" if net_debt < 0 else "Net Debt"
    net_debt_value = f"Rs {round(abs(net_debt)/1e9, 1)}K Cr"
    col5.metric(net_debt_label, net_debt_value)
    col6.metric("Current Ratio", f"{result['current_ratio']}x")
    col7.metric("Interest Cover", f"{result['interest_coverage']}x")
    col8.metric("ROE", f"{result['roe_pct']}%")

    st.markdown(f'<div class="grade-box"><span class="grade-text">{result["grade"]}</span><br><span class="grade-label">Aetas Credit Grade</span></div>', unsafe_allow_html=True)

    if result["leverage"] < 3:
        st.success("LOW LEVERAGE - STRONG CREDIT PROFILE")
    elif result["leverage"] < 5:
        st.warning("MODERATE LEVERAGE - MONITOR CLOSELY")
    else:
        st.error("HIGH LEVERAGE - ELEVATED CREDIT RISK")


def generate_memo(financials_summary):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a senior credit analyst at a private credit fund. Write concise, professional credit memos with three clearly labeled sections: Investment Thesis, Key Risks, Recommendation. Each section should be 2-3 sentences max. Use the financial ratios AND the recent news headlines provided to make the memo specific and grounded in real context, not generic."},
            {"role": "user", "content": f"Write a credit memo for the following company.\n\n{financials_summary}"}
        ]
    )
    return response.choices[0].message.content


mode = st.radio("Mode", ["Single Company", "Compare Two Companies"], horizontal=True, label_visibility="collapsed")
exchange = st.radio("Exchange", ["NSE", "BSE"], horizontal=True)

if mode == "Single Company":
    selected_company = st.selectbox("", options=list(companies.keys()), index=None, placeholder="Search for a company - e.g. HDFC Bank")
    generate = st.button("Generate")

    if generate:
        if not selected_company:
            st.warning("Please select a company.")
        else:
            ticker = companies[selected_company][exchange]
            with st.spinner("Pulling financials and generating memo..."):
                try:
                    result = analyze_company(ticker)
                    if result is None:
                        st.error("Data not available for this ticker. Try a different company.")
                    else:
                        render_metrics(result)
                        st.markdown('<div class="memo-label">Recent News</div>', unsafe_allow_html=True)
                        st.markdown(result["news_text"])
                        memo = generate_memo(result["financials_summary"])
                        st.markdown('<div class="memo-label">Credit Memo</div>', unsafe_allow_html=True)
                        st.markdown(memo)
                except Exception:
                    st.error("Could not retrieve data for this ticker. Please check the symbol and try again.")

else:
    col_a, col_b = st.columns(2)
    with col_a:
        company_a = st.selectbox("Company A", options=list(companies.keys()), index=None, placeholder="First company", key="company_a")
    with col_b:
        company_b = st.selectbox("Company B", options=list(companies.keys()), index=None, placeholder="Second company", key="company_b")

    compare = st.button("Compare")

    if compare:
        if not company_a or not company_b:
            st.warning("Please select both companies.")
        else:
            with st.spinner("Pulling financials and generating comparison..."):
                try:
                    ticker_a = companies[company_a][exchange]
                    ticker_b = companies[company_b][exchange]
                    result_a = analyze_company(ticker_a)
                    result_b = analyze_company(ticker_b)

                    if result_a is None or result_b is None:
                        st.error("Data not available for one or both companies. Try different selections.")
                    else:
                        render_metrics(result_a)
                        st.markdown('<div class="vs-divider">VS</div>', unsafe_allow_html=True)
                        render_metrics(result_b)

                        combined_summary = f"""
COMPANY A:
{result_a['financials_summary']}

COMPANY B:
{result_b['financials_summary']}
"""
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "You are a senior credit analyst at a private credit fund. Compare these two companies as credit risks. Write three sections: Comparative Summary (2-3 sentences), Stronger Credit Profile (state which company and why in 2-3 sentences), Key Differentiators (2-3 bullet points)."},
                                {"role": "user", "content": combined_summary}
                            ]
                        )
                        st.markdown('<div class="memo-label">Comparative Analysis</div>', unsafe_allow_html=True)
                        st.markdown(response.choices[0].message.content)
                except Exception:
                    st.error("Could not complete comparison. Please check your selections and try again.")

st.markdown('<div class="footer-text">Aetas - Built by Sahir Mendiratta</div>', unsafe_allow_html=True)