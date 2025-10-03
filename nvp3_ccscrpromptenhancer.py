import streamlit as st

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Prompt Enhancer", page_icon="📝")
st.title("📝 Prompt Engineer — CCSCR Prompt Enhancer")
st.caption("Demo Mode - Learn how to structure better prompts using CCSCR!")

# -------------------------------
# Input Sections (CCSCR)
# -------------------------------

# 1. Context Requirements
st.subheader("1️⃣ Context Requirements")
context_req = st.text_area(
    "Define domain, audience, goal, style preferences",
    value="Domain: Product Tech | Audience: busy professional | Goal: clarity | Tone: neutral"
)

# 2. Constraint Specifications
st.subheader("2️⃣ Constraint Specifications")
constraint_spec = st.text_area(
    "Enter constraints (compliance, tone, prohibited content, etc.)",
    value="No sensitive PII, comply with brand tone, concise language"
)

# 3. Structure Mandates
st.subheader("3️⃣ Structure Mandates")
structure_mandates = st.text_area(
    "Enter structure rules (formatting, output length, hierarchy)",
    value="3 concise bullets (≤12 words each), 1 clarifying question"
)

# 4. Checkpoint Integration
st.subheader("4️⃣ Checkpoint Integration")
checkpoint_integration = st.text_area(
    "Enter assumptions, risks, and validation steps",
    value="Flag uncertainties; human review if compliance risk; validate clarity"
)

# 5. Review Protocols
st.subheader("5️⃣ Review Protocols")
review_protocols = st.text_area(
    "Define review/approval points",
    value="Final approval by human reviewer; revision loops allowed"
)

# -------------------------------
# Draft Prompt Input
# -------------------------------
st.subheader("Paste your rough prompt")
draft = st.text_area("Your draft prompt:", height=140)

# -------------------------------
# Enhancement Button Logic
# -------------------------------
if st.button("Enhance Prompt"):
    if not draft.strip():
        st.warning("Please enter a draft prompt.")
    else:
        # Demo output showing CCSCR structure
        instruction = (
            "Generate an enhanced, structured prompt using CCSCR.\n"
            "1) Improve clarity and completeness\n"
            "2) Ask ONE clarifying question\n"
            "3) Specify output format (3 bullets, ≤12 words each)\n"
        )
        
        demo_output = (
            f"CONTEXT REQUIREMENTS:\n{context_req}\n\n"
            f"CONSTRAINT SPECIFICATIONS:\n{constraint_spec}\n\n"
            f"STRUCTURE MANDATES:\n{structure_mandates}\n\n"
            f"CHECKPOINT INTEGRATION:\n{checkpoint_integration}\n\n"
            f"REVIEW PROTOCOLS:\n{review_protocols}\n\n"
            f"USER DRAFT:\n{draft}\n\n"
            "OUTPUT FORMAT:\n- 3 concise bullets\n- 1 clarifying question"
        )
        
        st.success("Enhanced Prompt (Demo Mode)")
        st.code(instruction + "\n" + demo_output, language="markdown")
        
        st.info("💡 This is demo mode showing the CCSCR structure. In live mode, AI would generate the actual enhanced prompt!")
