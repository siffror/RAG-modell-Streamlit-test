# ui/file_loader.py
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber
from core.ocr_utils import extract_text_easyocr, extract_text_pytesseract, TESSERACT_INSTALLED

@st.cache_data(show_spinner=False)
def fetch_html_text(url):
    try:
        import requests
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return "\n".join(line.strip() for line in soup.get_text("\n").splitlines() if line.strip())
    except Exception as e:
        st.error(f"❌ Fel vid hämtning av HTML: {e}")
        return ""

def extract_text_from_file(file):
    text_output = ""
    if file.name.endswith(".pdf"):
        file.seek(0)
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_output += page_text + "\n"
        except Exception as e:
            st.warning(f"⚠️ Kunde inte läsa PDF: {e}")

    elif file.name.endswith(".html"):
        soup = BeautifulSoup(file.read(), "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text_output = soup.get_text(separator="\n")

    elif file.name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
        text_output = df.to_string(index=False)

    return text_output

def load_text_sources(html_link, uploaded_file, ocr_engine):
    preview, ocr_text = "", ""

    if uploaded_file:
        if uploaded_file.name.endswith((".png", ".jpg", ".jpeg", ".pdf")):
            if ocr_engine == "Tesseract" and not TESSERACT_INSTALLED:
                st.error("❌ Tesseract är inte installerat. Välj EasyOCR.")
                st.stop()

            if ocr_engine == "EasyOCR":
                ocr_text, _ = extract_text_easyocr(uploaded_file)
            else:
                ocr_text = extract_text_pytesseract(uploaded_file)

            if ocr_text.strip():
                st.text_area("📄 OCR-utläst text:", ocr_text[:3000], height=250)
            else:
                st.warning("⚠️ OCR kunde inte läsa någon text.")
        else:
            preview = extract_text_from_file(uploaded_file)

    elif html_link:
        preview = fetch_html_text(html_link)
    else:
        preview = st.text_area("✏️ Klistra in text manuellt här:", "", height=200)

    return preview or ocr_text, preview
