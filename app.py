# app.py
import streamlit as st
from ui.ocr_ui import handle_ocr_section
from ui.gpt_ui import handle_gpt_analysis
from ui.file_loader import load_text_sources

st.set_page_config(page_title="📊 AI Rapportanalys", layout="wide")
st.markdown("<h1 style='color:#3EA6FF;'>📊 AI-baserad Rapportanalys</h1>", unsafe_allow_html=True)
st.image("https://www.appypie.com/dharam_design/wp-content/uploads/2025/05/headd.svg", width=120)

# --- Ladda upp fil / länk / manuell text ---
html_link = st.text_input("🌐 Rapport-länk (HTML)")
uploaded_file = st.file_uploader("📎 Ladda upp HTML, PDF, Excel eller bild", type=["html", "pdf", "xlsx", "xls", "png", "jpg", "jpeg"])

ocr_engine = st.radio("🧠 Välj OCR-motor:", ["EasyOCR", "Tesseract"], horizontal=True)

# --- Extrahera text beroende på källa ---
text_to_analyze, preview = load_text_sources(html_link, uploaded_file, ocr_engine)

# --- Visa textpreview ---
if text_to_analyze:
    st.text_area("📄 Förhandsvisning:", text_to_analyze[:5000], height=200)
else:
    st.warning("❌ Ingen text att analysera än.")

# --- Fullständig rapportanalys ---
handle_gpt_analysis(text_to_analyze)

# --- Fråga GPT specifikt ---
handle_ocr_section(text_to_analyze)
