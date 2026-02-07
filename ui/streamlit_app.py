import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RAG Document Search",
    layout="centered",
)

st.title("📄 RAG Document Search")
st.caption("Query documents stored in Supabase using a Retrieval-Augmented Generation pipeline")

st.divider()

query = st.text_area(
    "Enter your question",
    placeholder="e.g. What is BERT and how does it work?",
    height=120,
)

top_k = st.slider(
    "Number of documents to retrieve",
    min_value=1,
    max_value=10,
    value=3,
)

if st.button("🔍 Run Query", type="primary"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Running RAG pipeline..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "query": query,
                        "top_k": top_k,
                    },
                    timeout=60,
                )

                if response.status_code == 200:
                    data = response.json()

                    st.subheader("🧠 Answer")
                    st.write(data["answer"])

                else:
                    st.error(
                        f"API error ({response.status_code}): {response.text}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. "
                    "Make sure FastAPI is running on http://localhost:8000"
                )
