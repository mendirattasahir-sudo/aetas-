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
    div[role="radiogroup"] {
        gap: 8px;
    }
    div[role="radiogroup"] label {
        background-color: #0a0a0a;
        border: 0.5px solid #2a2a2a;
        border-radius: 6px;
        padding: 8px 16px !important;
        margin: 0 !important;
    }
    div[role="radiogroup"] label:has(input:checked) {
        background-color: #ffffff;
        border-color: #ffffff;
    }
    div[role="radiogroup"] label:has(input:checked) p {
        color: #000000 !important;
    }
    div[role="radiogroup"] input {
        accent-color: #ffffff;
    }
    div[role="radiogroup"] p {
        color: #e5e5e5;
        font-size: 13px;
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
    "GAIL": "GAIL.NS",
}


def resolve_ticker(user_input):
    """Resolves a company name from the curated list, or treats the input as a raw ticker."""
    if user_input in companies:
        return companies[user_input]
    cleaned = user_input.strip().upper()
    if not cleaned:
        return None
    if "." not in cleaned:
        cleaned = cleaned + ".NS"
    return cleaned


def get_trend_data(stock):
    """Pulls up to 3 years of revenue, EBITDA and debt to detect direction of travel."""
    try:
        fin = stock.financials
        bs = stock.balance_sheet
        years = list(fin.columns[:3]) if not fin.empty else []

        trend_rows = []
        for year in years:
            try:
                rev = float(fin.loc['Total Revenue', year]) if 'Total Revenue' in fin.index else None
            except Exception:
                rev = None
            try:
                ebt = float(fin.loc['EBITDA', year]) if 'EBITDA' in fin.index else None
            except Exception:
                ebt = None
            try:
                debt = float(bs.loc['Total Debt', year]) if 'Total Debt' in bs.index else None
            except Exception:
                debt = None
            trend_rows.append({"year": str(year.year), "revenue": rev, "ebitda": ebt, "debt": debt})

        return trend_rows
    except Exception:
        return []


def summarize_trend(trend_rows):
    """Turns raw multi-year numbers into a plain-English description of what's changing."""
    if len(trend_rows) < 2:
        return "Insufficient historical data to establish a multi-year trend."

    oldest = trend_rows[-1]
    newest = trend_rows[0]
    lines = []

    if oldest.get("revenue") and newest.get("revenue"):
        rev_change = ((newest["revenue"] - oldest["revenue"]) / oldest["revenue"]) * 100
        lines.append(f"Revenue {'grew' if rev_change >= 0 else 'declined'} {abs(round(rev_change, 1))}% from {oldest['year']} to {newest['year']}.")

    if oldest.get("debt") and newest.get("debt"):
        debt_change = ((newest["debt"] - oldest["debt"]) / oldest["debt"]) * 100
        lines.append(f"Total debt {'increased' if debt_change >= 0 else 'decreased'} {abs(round(debt_change, 1))}% over the same period.")

    if oldest.get("ebitda") and newest.get("ebitda"):
        ebitda_change = ((newest["ebitda"] - oldest["ebitda"]) / oldest["ebitda"]) * 100
        lines.append(f"EBITDA {'grew' if ebitda_change >= 0 else 'declined'} {abs(round(ebitda_change, 1))}% over the same period.")

    if oldest.get("revenue") and newest.get("revenue") and oldest.get("debt") and newest.get("debt"):
        rev_change = ((newest["revenue"] - oldest["revenue"]) / oldest["revenue"]) * 100
        debt_change = ((newest["debt"] - oldest["debt"]) / oldest["debt"]) * 100
        if debt_change > rev_change + 10:
            lines.append("FLAG: Debt is growing meaningfully faster than revenue, a classic early warning sign of deteriorating credit quality.")

    return " ".join(lines) if lines else "Trend data available but incomplete for full analysis."


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

    trend_rows = get_trend_data(stock)
    trend_summary = summarize_trend(trend_rows)

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

3-Year Trend: {trend_summary}

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
        "trend_rows": trend_rows,
        "trend_summary": trend_summary,
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

    trend_rows = result.get("trend_rows", [])
    if len(trend_rows) >= 2:
        st.markdown('<div class="memo-label">3-Year Trend</div>', unsafe_allow_html=True)
        chart_data = {}
        years_sorted = list(reversed(trend_rows))
        labels = [r["year"] for r in years_sorted]
        revenues = [r["revenue"] / 1e7 if r["revenue"] else None for r in years_sorted]
        debts = [r["debt"] / 1e7 if r["debt"] else None for r in years_sorted]
        try:
            import pandas as pd
            chart_df = pd.DataFrame({"Revenue (Rs Cr)": revenues, "Total Debt (Rs Cr)": debts}, index=labels)
            st.line_chart(chart_df)
        except Exception:
            pass
        st.caption(result.get("trend_summary", ""))


def generate_memo(financials_summary):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a senior credit analyst at a private credit fund. Write concise, professional credit memos with three clearly labeled sections: Investment Thesis, Key Risks, Recommendation. Each section should be 2-3 sentences max. The 3-Year Trend line is the most important input - lead with what is CHANGING over time (improving or deteriorating), not just the current snapshot. If debt is growing faster than revenue or EBITDA, treat this as the central risk in your analysis. Use the recent news headlines to add real-world context, not generic language."},
            {"role": "user", "content": f"Write a credit memo for the following company.\n\n{financials_summary}"}
        ]
    )
    return response.choices[0].message.content


mode = st.radio("Mode", ["Single Company", "Compare Two Companies"], horizontal=True, label_visibility="collapsed")

st.caption("Pick from the list below, or type any NSE ticker directly (e.g. SAFARI, SADBHAV).")

if mode == "Single Company":
    selected_company = st.selectbox("", options=list(companies.keys()), index=None, placeholder="Search for a company - e.g. HDFC Bank", accept_new_options=True)
    generate = st.button("Generate")

    if generate:
        ticker = resolve_ticker(selected_company) if selected_company else None
        if not ticker:
            st.warning("Please pick a company or type a ticker.")
        else:
            with st.spinner("Pulling financials and generating memo..."):
                try:
                    result = analyze_company(ticker)
                    if result is None:
                        st.error("Data not available for this ticker. Check the symbol and try again.")
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
        company_a = st.selectbox("Company A", options=list(companies.keys()), index=None, placeholder="First company", accept_new_options=True, key="company_a")
    with col_b:
        company_b = st.selectbox("Company B", options=list(companies.keys()), index=None, placeholder="Second company", accept_new_options=True, key="company_b")

    compare = st.button("Compare")

    if compare:
        ticker_a = resolve_ticker(company_a) if company_a else None
        ticker_b = resolve_ticker(company_b) if company_b else None

        if not ticker_a or not ticker_b:
            st.warning("Please select or type both companies.")
        else:
            with st.spinner("Pulling financials and generating comparison..."):
                try:
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