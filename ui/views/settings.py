import streamlit as st
import requests
from services.settings import settings_service

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
    
    # Load current settings from backend
    use_nvidia = False
    nvidia_api_key = ""
    nvidia_llm = "meta/llama-3.1-70b-instruct"
    nvidia_emb = "nvidia/llama-nemotron-embed-vl-1b-v2"
    
    try:
        resp = settings_service.get(st.session_state.token)
        if resp.status_code == 200:
            cfg = resp.json()
            use_nvidia = cfg.get("use_nvidia", False)
            nvidia_api_key = cfg.get("nvidia_api_key") or ""
            nvidia_llm = cfg.get("nvidia_llm_model") or "meta/llama-3.1-70b-instruct"
            nvidia_emb = cfg.get("nvidia_embedding_model") or "nvidia/llama-nemotron-embed-vl-1b-v2"
    except Exception as e:
        st.error(f"Failed to load configuration from backend: {e}")

    # Settings form
    with st.form("settings_form"):
        mode = st.radio(
            "AI Provider Mode",
            options=["Local (Ollama + SentenceTransformer)", "NVIDIA Cloud (NVIDIA AI Endpoints)"],
            index=1 if use_nvidia else 0
        )
        
        st.write("---")
        st.subheader("NVIDIA AI Endpoints Settings")
        key = st.text_input("NVIDIA API Key", value=nvidia_api_key, type="password", placeholder="nvapi-...")
        llm_model = st.text_input("NVIDIA Chat LLM Model", value=nvidia_llm)
        emb_model = st.text_input("NVIDIA Embedding Model", value=nvidia_emb)
        
        submit = st.form_submit_button("Save & Apply Configuration", use_container_width=True)
        if submit:
            payload = {
                "use_nvidia": mode == "NVIDIA Cloud (NVIDIA AI Endpoints)",
                "nvidia_api_key": key if key else None,
                "nvidia_llm_model": llm_model,
                "nvidia_embedding_model": emb_model
            }
            try:
                upd_resp = settings_service.update(st.session_state.token, payload)
                if upd_resp.status_code == 200:
                    st.success("Configuration updated and applied successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to update configuration: {upd_resp.text}")
            except Exception as e:
                st.error(f"Error saving settings: {e}")

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
