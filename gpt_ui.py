# ui/gpt_ui.py
import streamlit as st
from core.gpt_logic import full_rapportanalys

def handle_gpt_analysis(text_to_analyze):
    st.markdown("---")
    st.markdown("### 🧾 Fullständig rapportanalys")

    if st.button("📊 Kör full analys"):
        if text_to_analyze:
            with st.spinner("GPT analyserar hela rapporten..."):
                result = full_rapportanalys(text_to_analyze)
                st.markdown(result)
        else:
            st.error("❌ Ingen text tillgänglig för analys.")
