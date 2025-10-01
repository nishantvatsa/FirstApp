import streamlit as st

st.set_page_config(page_title="Context Enhancer (CC-SC-R)", page_icon="📝")
st.title("📝 Context Engineer — CC-SC-R Prompt Enhancer by NV")
st.caption("Demo Mode — Learn how to structure better prompts with CC-SC-R")

# ──────────────────────────────────────────────────────────────────────────────
# Role & Meta (kept simple for beginners)
# ──────────────────────────────────────────────────────────────────────────────
st.subheader("Set Role (Optional)")
role = st.text_input("Role", value="an experienced software developer mentoring a beginner")

# ──────────────────────────────────────────────────────────────────────────────
# CC-SC-R Framework Inputs
# ──────────────────────────────────────────────────────────────────────────────
st.subheader("CC-SC-R Framework")

with st.expander("Context Requirements", expanded=True):
    ctx_domain = st.text_input("Domain", value="Demo apps with Streamlit")
    ctx_audience = st.text_input("Audience", value="Beginner, non-tech user")
    ctx_goals = st.text_area("Goals", value="Make rough prompts clearer and more actionable")
    ctx_data_sources = st.text_area("Data Sources", value="User’s pasted draft only (no external APIs)")

with st.expander("Constraint Specifications", expanded=True):
    cons_policies = st.text_area("Policies / Compliance", value="No external API calls; demo use only")
    cons_tone = st.text_input("Tone guidelines", value="Simple, friendly, direct")
    cons_env = st.text_area(
        "Environment",
        value="Streamlit (local), Python (local), VS Code on macOS"
    )

with st.expander("Structure Mandates", expanded=True):
    struct_sections = st.text_area(
        "Required sections",
        value="- Reformulated Prompt\n- Key Assumptions\n- One Clarifying Question\n- Output Format"
    )
    struct_formatting = st.text_area(
        "Formatting / Organization",
        value="Use concise bullets; ≤12 words per bullet where possible"
    )

with st.expander("Checkpoint Integration", expanded=True):
    cp_assumptions = st.text_area("Assumptions", value="User wants clarity; no external tools needed")
    cp_risks = st.text_area("Risks", value="Ambiguous draft; missing context; over-constraint")
    cp_confidence = st.slider("Confidence level (demo)", min_value=0, max_value=100, value=70)

with st.expander("Review Protocols", expanded=True):
    rev_human = st.text_area(
        "Human approval / edits",
        value="User reviews and edits before using the prompt"
    )
    rev_accountability = st.text_area(
        "Accountability",
        value="This is a demo aid; user is owner of final prompt"
    )

# ──────────────────────────────────────────────────────────────────────────────
# Rough Prompt
# ──────────────────────────────────────────────────────────────────────────────
st.subheader("Paste your rough prompt")
draft = st.text_area("Your draft prompt:", height=160)

# ──────────────────────────────────────────────────────────────────────────────
# Enhance (Demo Mode)
# ──────────────────────────────────────────────────────────────────────────────
if st.button("Enhance Prompt (Demo Mode)"):
    if not draft.strip():
        st.warning("Please enter a draft prompt.")
    else:
        # Instruction block describing how to use CC-SC-R to transform the draft
        instruction = (
            "Generate an enhanced, structured prompt using the CC-SC-R framework.\n"
            "Follow these rules strictly:\n"
            "1) Use the provided Context Requirements to ground the prompt.\n"
            "2) Respect all Constraint Specifications (policies, tone, environment).\n"
            "3) Enforce the Structure Mandates (sections + formatting).\n"
            "4) Include Checkpoint Integration: summarize assumptions, risks, confidence.\n"
            "5) Add Review Protocols: note human approval and edit expectations.\n"
            "6) Ask EXACTLY ONE clarifying question.\n"
            "7) Output format: 3 concise bullets (≤12 words each) under 'Reformulated Prompt'."
        )

        # Demo payload showing what the model would see in a real run
        payload = (
            f"ROLE: {role}\n\n"
            "CC-SC-R INPUTS\n"
            "— Context Requirements —\n"
            f"Domain: {ctx_domain}\n"
            f"Audience: {ctx_audience}\n"
            f"Goals: {ctx_goals}\n"
            f"Data Sources: {ctx_data_sources}\n\n"
            "— Constraint Specifications —\n"
            f"Policies/Compliance: {cons_policies}\n"
            f"Tone: {cons_tone}\n"
            f"Environment: {cons_env}\n\n"
            "— Structure Mandates —\n"
            f"Required Sections:\n{struct_sections}\n\n"
            f"Formatting/Organization:\n{struct_formatting}\n\n"
            "— Checkpoint Integration —\n"
            f"Assumptions:\n{cp_assumptions}\n\n"
            f"Risks:\n{cp_risks}\n\n"
            f"Confidence: {cp_confidence}%\n\n"
            "— Review Protocols —\n"
            f"Human Approval / Edits:\n{rev_human}\n\n"
            f"Accountability:\n{rev_accountability}\n\n"
            "USER DRAFT:\n"
            f"{draft}\n\n"
            "OUTPUT SPEC:\n"
            "- 'Reformulated Prompt' section: 3 bullets, ≤12 words each\n"
            "- 'One Clarifying Question' section: exactly one question\n"
            "- 'Assumptions & Risks' section: brief bullets"
        )

        st.success("Enhanced Prompt (Demo Mode)")
        st.code(instruction + "\n\n" + payload, language="markdown")

        st.info("💡 This is demo mode showing the CC-SC-R structure. In live mode, AI would generate the actual enhanced prompt content.")

# ──────────────────────────────────────────────────────────────────────────────
# Footer helper
# ──────────────────────────────────────────────────────────────────────────────
st.caption("Tip: Run locally via `streamlit run app.py`. No APIs required.")
