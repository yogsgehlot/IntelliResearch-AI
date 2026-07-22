import streamlit as st
import requests

def render():
    st.title("⚙️ Settings")
    
    st.subheader("System Information")
    
    # Try fetching system backend info
    try:
        response = requests.get("http://localhost:8000/api/v1/version", timeout=2)
        if response.status_code == 200:
            sys_info = response.json()
            st.success(f"Connected to Backend: **{sys_info.get('project', 'IntelliResearch-AI')}**")
            st.info(f"API Version: `{sys_info.get('version', 'unknown')}`")
        else:
            st.warning("Backend API responded with an error.")
    except Exception:
        st.error("Could not connect to backend server. Make sure it is running on http://localhost:8000")

    st.divider()

    st.subheader("AI Configuration")
    st.markdown("""
    - **Active LLM Model**: `llama3.2` (via Local Ollama)
    - **Active Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional dense vectors)
    - **Vector Store Engine**: Local FAISS (Thread-Safe File Index)
    - **Hybrid Search Components**: FAISS Semantic Vectors + BM25 Lexical Keyword Store
    """)

    st.divider()

    st.subheader("User Account")
    user = st.session_state.get("user")
    if user:
        st.markdown(f"""
        - **Email**: {user.get('email', 'N/A')}
        - **Status**: Authenticated
        """)
        
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.token = None
        st.session_state.user = None
        st.session_state.project = None
        st.rerun()
