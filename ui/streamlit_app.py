import os
import requests
import streamlit as st

# Support both local development and Docker deployment
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="RAG Document Search",
    layout="centered",
)

st.title("📄 RAG Document Search")
st.caption("Query documents stored in Supabase using a Retrieval-Augmented Generation pipeline")

st.divider()

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.caption(f"API: {API_URL}")
    
    llm_model = st.selectbox(
        "Select LLM Model",
        options=[
            "google/flan-t5-small",
            "google/flan-t5-base",
            "google/flan-t5-large",
            "gpt-3.5-turbo",
            "gpt-4",
        ],
        index=0,
        help="Choose the language model for generation"
    )
    
    st.divider()
    st.markdown("### About")
    st.markdown("""
    This RAG system retrieves relevant document chunks 
    and generates answers using LLMs.
    
    **Features:**
    - Dense vector retrieval (FAISS)
    - Multiple LLM backends
    - Token-aware context sizing
    """)

query = st.text_area(
    "Enter your question",
    placeholder="e.g. What is BERT and how does it work?",
    height=120,
)

top_k = st.slider(
    "Number of documents to retrieve",
    min_value=1,
    max_value=10,
    value=5,
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
                        "llm_model": llm_model if llm_model != "google/flan-t5-small" else None,
                    },
                    timeout=60,
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("✅ Query completed successfully!")
                    
                    # Display answer
                    st.subheader("🧠 Answer")
                    st.markdown(data["answer"])
                    
                    # Display metadata
                    with st.expander("📊 Query Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Model Used", data.get("model", "N/A"))
                        with col2:
                            st.metric("Documents Retrieved", data.get("top_k", "N/A"))
                        
                        st.caption(f"**Query:** {data.get('query', query)}")

                else:
                    st.error(
                        f"API error ({response.status_code}): {response.text}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    f"❌ Could not connect to the API at {API_URL}. "
                    "Make sure the backend is running."
                )
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The query may be taking too long.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
