# ui/ocr_ui.py
import streamlit as st
from core.ocr_utils import TESSERACT_INSTALLED
import shutil

def handle_ocr_section(text_to_analyze):
    st.markdown("---")
    st.markdown("### 🧠 GPT-fråga på innehållet")

    if "user_question" not in st.session_state:
        st.session_state.user_question = "Vilken utdelning per aktie föreslås?"

    st.text_input("Fråga:", key="user_question")

    if text_to_analyze and len(text_to_analyze.strip()) > 20:
        if st.button("🔍 Analysera med GPT"):
            from core.gpt_logic import (
                get_embedding_cache_name, load_embeddings_if_exists, chunk_text,
                get_embedding, save_embeddings, search_relevant_chunks,
                generate_gpt_answer, is_key_figure
            )

            with st.spinner("🤖 GPT analyserar..."):
                source_id = "manual-entry-v1"
                cache_file = get_embedding_cache_name(source_id)
                embedded_chunks = load_embeddings_if_exists(cache_file)

                if not embedded_chunks:
                    chunks = chunk_text(text_to_analyze)
                    embedded_chunks = []
                    for i, chunk in enumerate(chunks, 1):
                        st.write(f"🔹 Chunk {i} – {len(chunk)} tecken")
                        try:
                            embedding = get_embedding(chunk)
                            embedded_chunks.append({"text": chunk, "embedding": embedding})
                        except Exception as e:
                            st.error(f"❌ Fel vid embedding av chunk {i}: {e}")
                            st.stop()
                    save_embeddings(cache_file, embedded_chunks)

                context, top_chunks = search_relevant_chunks(st.session_state.user_question, embedded_chunks)
                st.code(context[:1000], language="text")
                answer = generate_gpt_answer(st.session_state.user_question, context)

                st.success("✅ Svar klart!")
                st.markdown(f"### 🤖 GPT-4o svar:\n{answer}")

                key_figures = [row for row in answer.split("\n") if is_key_figure(row)]
                if key_figures:
                    st.markdown("### 📊 Möjliga nyckeltal i svaret:")
                    for row in key_figures:
                        st.markdown(f"- {row}")

                from fpdf import FPDF
                st.download_button("💾 Ladda ner svar (.txt)", answer, file_name="gpt_svar.txt")
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in answer.split("\n"):
                    pdf.multi_cell(0, 10, line)
                st.download_button("📄 Ladda ner svar (.pdf)", pdf.output(dest="S").encode("latin1"), file_name="gpt_svar.pdf")

    else:
        st.info("📝 Ange text först för att kunna ställa en GPT-fråga.")

    if TESSERACT_INSTALLED:
        st.caption(f"🧠 Tesseract finns: {shutil.which('tesseract')}")
