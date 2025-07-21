import streamlit as st
import requests
import yaml

st.title("GenAI Accounting PoC")

api_url = st.text_input("API URL", value="http://localhost:8000")

tab = st.tabs(["Generate Case", "Search Cases"])[0]

with tab:
    st.subheader("Generate New Case")
    meta_yaml = st.text_area("Paste YAML Metadata", height=300, value="""case_id: test-001
case_title: IFRS 16 Lease Test
learning_objectives:
  - Determine ROU asset and lease liability
difficulty: intro
estimated_time_min: 45
scenario_context:
  industry: SaaS
  fiscal_year: 2025
  reporting_currency: JPY
key_figures:
  revenue: 560000000
  cogs: 310000000""")
    if st.button("Generate"):
        resp = requests.post(f"{api_url}/generate", json={"yaml_meta": meta_yaml},timeout=60)
        if resp.ok:
            st.success("Generated!")
            st.json(resp.json())
        else:
            st.error(resp.text)

with st.tabs(["Generate Case", "Search Cases"])[1]:
    st.subheader("Search Cases")
    query = st.text_input("Enter search query")
    if st.button("Search"):
        resp = requests.post(f"{api_url}/search", json={"query": query})
        if resp.ok:
            st.json(resp.json())
        else:
            st.error(resp.text)