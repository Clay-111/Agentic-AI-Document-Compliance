import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
from orchestrator import orchestrate, export_report_to_excel

st.set_page_config(page_title="Compliance Validator", layout="wide")

st.title("📄 Document Compliance Validator")
st.markdown("Upload PDF files into the `sample_docs/` folder and click below to run validation.")

if st.button("🚀 Run Validation"):
    vres, dres = orchestrate()
    export_report_to_excel(vres, dres)

    st.success("Validation complete! Check `reports/compliance_report.xlsx`.")

    with st.expander("🔍 View Results"):
        st.write("### Validation Issues")
        st.json(vres)

        st.write("### Discrepancies")
        st.json(dres)
