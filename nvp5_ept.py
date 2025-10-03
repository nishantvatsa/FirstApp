import os
import requests
import streamlit as st

# --------------------------------------------
# Page setup
# --------------------------------------------
st.set_page_config(page_title="Equity Metrics (CCSCR)", page_icon="📈", layout="centered")
st.title("📈 Equity Metrics — CCSCR Prompt")
st.caption("Demo app: PE / P/B / Dividend Yield / ROE. If API unavailable → returns NA.")

# ============================================
# 1) CONTEXT REQUIREMENTS
# ============================================
st.subheader("1️⃣ Context Requirements")
context_requirements = st.text_area(
    "Define domain, audience, goal, and style",
    value="Domain: Equity fundamentals | Audience: Retail investor | Goal: Snapshot of ratios | Style: concise"
)

# ============================================
# 2) CONSTRAINT SPECIFICATIONS
# ============================================
st.subheader("2️⃣ Constraint Specifications")
constraint_spec = st.text_area(
    "Constraints and data-source rules",
    value="If API missing, fallback to NA values. No PII. Info only."
)

# Sidebar: API Keys (optional)
st.sidebar.header("🔐 API Keys (Optional)")
ALPHAVANTAGE_API_KEY = st.sidebar.text_input("Alpha Vantage API Key", value="", type="password")
FINNHUB_API_KEY = st.sidebar.text_input("Finnhub API Key", value="", type="password")

# ============================================
# 3) STRUCTURE MANDATES
# ============================================
st.subheader("3️⃣ Structure Mandates")
structure_mandates = st.text_area(
    "Specify structure",
    value="Inputs: Company Name | Outputs: PE, Sector PE, P/B, Dividend Yield, ROE"
)

# ============================================
# 4) CHECKPOINT INTEGRATION
# ============================================
st.subheader("4️⃣ Checkpoint Integration")
checkpoint_integration = st.text_area(
    "Assumptions, risks, QA plan",
    value="If API not available, return NA safely. User validates ticker."
)

# ============================================
# 5) REVIEW PROTOCOLS
# ============================================
st.subheader("5️⃣ Review Protocols")
review_protocols = st.text_area(
    "Define review process",
    value="Cross-verify values with broker portals before investment decisions."
)

st.divider()

# ============================================
# INPUT: Company Name
# ============================================
st.subheader("🔎 Company Search")
company_query = st.text_input("Enter Company Name", value="Bajaj Finance")
go = st.button("Fetch Metrics")

# ============================================
# Helper functions
# ============================================
def safe_float(x):
    try:
        return float(x) if x not in (None, "None", "", "NA", "nan") else None
    except Exception:
        return None

def dummy_data():
    """Fallback if API not available"""
    return {
        "Company": company_query,
        "PE": "NA",
        "Sector PE": "NA",
        "P/B": "NA",
        "Dividend Yield": "NA",
        "ROE": "NA"
    }

def fetch_data(symbol: str):
    """Fetch from Alpha Vantage (Overview). Fallback → dummy."""
    if not ALPHAVANTAGE_API_KEY:
        return dummy_data()
    try:
        url = "https://www.alphavantage.co/query"
        params = {"function": "OVERVIEW", "symbol": symbol, "apikey": ALPHAVANTAGE_API_KEY}
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        return {
            "Company": data.get("Name", company_query),
            "PE": data.get("PERatio", "NA"),
            "Sector PE": "NA",  # left as NA unless computed separately
            "P/B": data.get("PriceToBookRatio", "NA"),
            "Dividend Yield": data.get("DividendYield", "NA"),
            "ROE": data.get("ReturnOnEquityTTM", "NA")
        }
    except Exception:
        return dummy_data()

# ============================================
# Main Logic
# ============================================
if go:
    result = fetch_data(company_query)

    # ---- Display ----
    st.subheader("📊 Result")
    st.write(f"**Company:** {result['Company']}")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("P/E", result["PE"])
        st.metric("P/B", result["P/B"])
    with col2:
        st.metric("Dividend Yield", result["Dividend Yield"])
        st.metric("ROE", result["ROE"])
    st.metric("Sector PE", result["Sector PE"])

    st.info("ℹ️ This demo shows NA if API not provided. Plug in API keys for live data.")
