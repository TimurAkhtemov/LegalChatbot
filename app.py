import streamlit as st
from rag_pipeline import get_answer

st.set_page_config(page_title="NJ Legal Q&A", layout="wide")
st.title("📘 New Jersey Legal Q&A Chatbot")
st.markdown("Ask a question based on New Jersey law. I’ll retrieve the most relevant statutes and provide a grounded response.")

user_question = st.text_input("🔍 Ask your legal question:")

if user_question:
    with st.spinner("Looking through New Jersey law..."):
        answer, metadatas = get_answer(user_question)
        st.markdown("### 📄 Answer")
        st.write(answer)

        st.markdown("---")
        st.markdown("### 📚 Source Sections")
        for meta in metadatas:
            st.markdown(f"- **{meta['section']}**: {meta['heading']}")
            st.markdown(f"[View Full Statute]({meta.get('source_url', '#')})")