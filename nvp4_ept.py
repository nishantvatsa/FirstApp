# ============================================
# 🧩 CCSCR Equity Metrics Fetcher (Streamlit)
# --------------------------------------------
# What this app does:
# - Input: Company name (e.g., "Bajaj Finance")
# - Output: PE, Sector PE (approx*), P/B, Dividend Yield, ROE
# - Provider: Alpha Vantage (Company OVERVIEW)
# - Optional Sector PE approx: Finnhub peers + Alpha Vantage PERatio avg
#
# *Sector PE "approx" is computed as the average PE of peers (if enabled).
#   It is a proxy and may differ from official “Industry/Sector PE” on portals.
#
# Setup:
#   pip install streamlit requests
#   streamlit run app.py
#
# NOTE: You need API keys:
#   - Alpha Vantage (free): https://www.alphavantage.co/support/#api-key
#   - Finnhub (optional, free tier): https://finnhub.io/
#
# ============================================

import os
import time
import requests
import streamlit as st

# --------------------------------------------
# Page setup
# --------------------------------------------
st.set_page_config(page_title="Equity Metrics (CCSCR)", page_icon="📈", layout="centered")
st.title("📈 Equity Metrics — CCSCR Prompt")
st.caption("Demo app for getting PE / P/B / Dividend Yield / ROE. Sector PE is optional (computed via peers).")

# ============================================
# 1) CONTEXT REQUIREMENTS (C1)
#    Domain, audience, goal, style
# ============================================
st.subheader("1️⃣ Context Requirements")
default_context = (
    "Domain: Equity fundamentals | Audience: Retail investor | "
    "Goal: Quick snapshot of key valuation ratios | Style: neutral, concise"
)
context_requirements = st.text_area(
    "Define domain, audience, goal, and style",
    value=default_context,
    help="This is meta-context to keep outputs consistent and auditable."
)

# ============================================
# 2) CONSTRAINT SPECIFICATIONS (C2)
#    Policies, data sources, compliance, limits
# ============================================
st.subheader("2️⃣ Constraint Specifications")
default_constraints = (
    "Use Alpha Vantage for ratios (OVERVIEW).\n"
    "Optionally use Finnhub to get peers and average their PE as sector proxy.\n"
    "Respect API rate limits (AV free ~5 req/min). Handle missing/NA fields safely.\n"
    "No PII. Data is for information only; not investment advice."
)
constraint_spec = st.text_area(
    "Enter constraints and data-source rules",
    value=default_constraints,
)

# Sidebar: API Keys and Options
st.sidebar.header("🔐 API & Options")
ALPHAVANTAGE_API_KEY = st.sidebar.text_input("Alpha Vantage API Key", value=os.getenv("ALPHAVANTAGE_API_KEY", ""), type="password")
FINNHUB_API_KEY = st.sidebar.text_input("Finnhub API Key (optional, for peers)", value=os.getenv("FINNHUB_API_KEY", ""), type="password")
compute_sector_pe = st.sidebar.checkbox("Compute Sector PE (approx via peers & AV)", value=False)
exchange_hint = st.sidebar.selectbox(
    "Exchange hint (helps symbol resolution)",
    ["Auto", "India (NSE/BSE)", "US", "Other"],
    index=0
)

# ============================================
# 3) STRUCTURE MANDATES (S)
#    Output fields, formatting, presentation
# ============================================
st.subheader("3️⃣ Structure Mandates")
default_structure = (
    "Inputs: Company Name\n"
    "Outputs: PE (PERatio), Sector PE (approx), PriceToBook (P/B), DividendYield, ReturnOnEquityTTM (ROE)\n"
    "Formatting: one result card with labeled rows; NA if unavailable"
)
structure_mandates = st.text_area(
    "Specify structure (fields, formatting, length)",
    value=default_structure,
)

# ============================================
# 4) CHECKPOINT INTEGRATION (C4)
#    Assumptions, risks, mitigations, QA
# ============================================
st.subheader("4️⃣ Checkpoint Integration")
default_checkpoint = (
    "Assumptions: Alpha Vantage OVERVIEW exposes PERatio, PriceToBookRatio, DividendYield, ReturnOnEquityTTM. "
    "Sector PE is approximated as mean peer PE.\n"
    "Risks: Symbol resolution ambiguity; API rate limits; data freshness; missing fields.\n"
    "Mitigation: Use SYMBOL_SEARCH; show top matches to pick; return NA on missing; throttle requests.\n"
    "QA: Echo raw symbol used; display provider and timestamp."
)
checkpoint_integration = st.text_area(
    "Assumptions, risks, and QA plan",
    value=default_checkpoint,
)

# ============================================
# 5) REVIEW PROTOCOLS (R)
#    Human approval & logging
# ============================================
st.subheader("5️⃣ Review Protocols")
default_review = (
    "User validates that resolved ticker is correct.\n"
    "If numbers materially differ from broker/portal, cross-check on official filings.\n"
    "Log provider, endpoints, and any fallbacks for audit."
)
review_protocols = st.text_area("Define review & approval process", value=default_review)

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

def av_symbol_search(keywords: str, apikey: str):
    """Use Alpha Vantage SYMBOL_SEARCH to find best-matching tickers."""
    url = "https://www.alphavantage.co/query"
    params = {"function": "SYMBOL_SEARCH", "keywords": keywords, "apikey": apikey}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def av_company_overview(symbol: str, apikey: str):
    """Use Alpha Vantage OVERVIEW to fetch fundamental ratios."""
    url = "https://www.alphavantage.co/query"
    params = {"function": "OVERVIEW", "symbol": symbol, "apikey": apikey}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def finnhub_company_peers(symbol: str, apikey: str):
    """Get peer tickers from Finnhub (if key provided)."""
    url = "https://finnhub.io/api/v1/stock/peers"
    params = {"symbol": symbol, "token": apikey}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json() if r.text else []

def infer_exchange_suffix(name_hint: str, raw_symbol: str) -> str:
    """
    Try to help with Indian symbols that typically require .NS / .BSE on some providers.
    For Alpha Vantage, use the exact symbol returned by SYMBOL_SEARCH (bestMatch["1. symbol"]).
    This function only tweaks if user chose an explicit hint.
    """
    if name_hint.startswith("India"):
        # Prefer NSE if available in search results; else return as-is
        # (We keep conservative here—SYMBOL_SEARCH output should already give proper symbol)
        return raw_symbol
    # For US/Other or Auto, keep as-is
    return raw_symbol

def safe_float(x):
    try:
        return float(x) if x not in (None, "None", "", "NA", "nan") else None
    except Exception:
        return None

# ============================================
# Main action
# ============================================
if go:
    if not ALPHAVANTAGE_API_KEY:
        st.error("Please provide an Alpha Vantage API key in the sidebar.")
        st.stop()

    # ---- Step 1: Symbol search and user confirmation ----
    try:
        search = av_symbol_search(company_query, ALPHAVANTAGE_API_KEY)
    except Exception as e:
        st.error(f"Search error: {e}")
        st.stop()

    matches = search.get("bestMatches", [])
    if not matches:
        st.warning("No matches found. Try a different name or add exchange (e.g., 'TCS NSE').")
        st.stop()

    # List top options for clarity
    st.write("**Top Symbol Matches (Alpha Vantage)**")
    options = []
    for m in matches[:5]:
        sym = m.get("1. symbol", "")
        name = m.get("2. name", "")
        region = m.get("4. region", "")
        currency = m.get("8. currency", "")
        options.append(f"{sym} — {name} [{region} | {currency}]")
    pick = st.selectbox("Select the intended symbol", options, index=0)

    selected_symbol = pick.split(" — ")[0].strip()
    selected_symbol = infer_exchange_suffix(exchange_hint, selected_symbol)

    st.info(f"Using Symbol: **{selected_symbol}**  | Provider: Alpha Vantage")

    # ---- Step 2: Fetch core metrics via OVERVIEW ----
    try:
        overview = av_company_overview(selected_symbol, ALPHAVANTAGE_API_KEY)
    except Exception as e:
        st.error(f"Overview fetch error: {e}")
        st.stop()

    # Parse key fields (Alpha Vantage field names)
    pe = safe_float(overview.get("PERatio"))
    pb = safe_float(overview.get("PriceToBookRatio"))
    div_yield = safe_float(overview.get("DividendYield"))
    roe_ttm = safe_float(overview.get("ReturnOnEquityTTM"))

    # ---- Step 3: Optional Sector PE (approx via peers) ----
    sector_pe = None
    peer_debug = []
    if compute_sector_pe and FINNHUB_API_KEY:
        try:
            peers = finnhub_company_peers(selected_symbol, FINNHUB_API_KEY)
            # Limit number of peers to be gentle with AV rate limits (e.g., first 6)
            peers = [p for p in peers if isinstance(p, str) and p.upper() != selected_symbol.upper()][:6]
            peer_pes = []
            for p in peers:
                try:
                    time.sleep(12)  # AV free tier ~5 calls/min; be conservative
                    ov = av_company_overview(p, ALPHAVANTAGE_API_KEY)
                    ppe = safe_float(ov.get("PERatio"))
                    if ppe and ppe > 0:
                        peer_pes.append(ppe)
                        peer_debug.append((p, ppe))
                except Exception as _:
                    continue
            if peer_pes:
                sector_pe = sum(peer_pes) / len(peer_pes)
        except Exception as e:
            st.warning(f"Peer-based Sector PE failed: {e}")

    # ---- Step 4: Display result card ----
    st.subheader("📊 Result")
    st.write(f"**Company:** {overview.get('Name', 'N/A')}  \n**Symbol:** `{selected_symbol}`")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("P/E (PERatio)", f"{pe:.2f}" if pe is not None else "NA")
        st.metric("P/B (PriceToBook)", f"{pb:.2f}" if pb is not None else "NA")
    with col2:
        st.metric("Dividend Yield", f"{div_yield:.2%}" if div_yield is not None else "NA")
        st.metric("ROE (TTM)", f"{roe_ttm:.2%}" if roe_ttm is not None else "NA")

    st.metric("Sector PE (approx via peers)", f"{sector_pe:.2f}" if sector_pe is not None else "NA")

    # ---- Step 5: Trace / Debug for auditability ----
    with st.expander("🔎 Debug / Trace (for audit)"):
        st.write("**Alpha Vantage OVERVIEW raw keys available:**")
        st.code(", ".join(sorted(list(overview.keys()))))
        if peer_debug:
            st.write("**Peer PEs used for Sector PE approx:**")
            for p, val in peer_debug:
                st.write(f"- {p}: {val:.2f}")
        st.caption("Timestamp: fetched at runtime | All values depend on provider refresh cycles.")

    st.success("Done. Please cross-verify numbers with filings if using for decisions.")
