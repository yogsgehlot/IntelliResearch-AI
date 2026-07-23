import streamlit as st
from services.projects import project_service
from services.documents import document_service
from services.notes import notes_service

def render():
    # Load stats
    total_projects = 0
    total_docs = 0
    active_project = st.session_state.get("project")
    active_project_notes = 0

    try:
        proj_resp = project_service.list(st.session_state.token)
        if proj_resp.status_code == 200:
            total_projects = len(proj_resp.json())
    except Exception:
        pass

    try:
        doc_resp = document_service.list(st.session_state.token)
        if doc_resp.status_code == 200:
            all_docs = doc_resp.json()
            total_docs = len(all_docs)
            # If a project is active, filter documents count for the current project
            if active_project:
                active_project_docs = len([d for d in all_docs if d.get("project_id") == active_project["id"]])
            else:
                active_project_docs = 0
    except Exception:
        total_docs = 0
        active_project_docs = 0

    if active_project:
        try:
            notes_resp = notes_service.list(st.session_state.token, active_project["id"])
            if notes_resp.status_code == 200:
                active_project_notes = len(notes_resp.json())
        except Exception:
            pass

    # Header Card with Premium Gradient
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">🏠 IntelliResearch AI Dashboard</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Your AI-Powered Research Assistant. Analyze documents, compile summaries, and organize insights.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Metrics Section
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.metric(
            label="📁 Total Projects",
            value=total_projects,
            help="Total research projects created in your workspace."
        )
        
    with m_col2:
        st.metric(
            label="📄 Uploaded Documents",
            value=total_docs,
            help="Total research papers, resumes, or manuals uploaded globally."
        )
        
    with m_col3:
        project_name = active_project["name"] if active_project else "None Selected"
        st.metric(
            label="📂 Active Project",
            value=project_name,
            help="The project currently selected in the sidebar."
        )

    st.divider()

    # Active Project / Getting Started Section
    if active_project:
        st.subheader(f"📂 Active Project Workspace: {active_project['name']}")
        
        # Project Details Card
        with st.container(border=True):
            st.markdown(f"**Description**:\n{active_project.get('description', 'No description provided.')}")
            
            # Active Project specific metrics
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.info(f"📄 **Documents in this Project**: {active_project_docs}")
            with p_col2:
                st.info(f"📒 **Notes in this Project**: {active_project_notes}")

        st.write("")
        st.markdown("### ⚡ Quick Navigation")
        
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
        
        with nav_col1:
            if st.button("💬 Chat / RAG", use_container_width=True, type="primary"):
                st.session_state.page = "Chat"
                st.rerun()
                
        with nav_col2:
            if st.button("📝 Summarizer", use_container_width=True):
                st.session_state.page = "Summary"
                st.rerun()
                
        with nav_col3:
            if st.button("📒 Notes Manager", use_container_width=True):
                st.session_state.page = "Notes"
                st.rerun()

        with nav_col4:
            if st.button("📄 Manage Documents", use_container_width=True):
                st.session_state.page = "Upload"
                st.rerun()
                
    else:
        # Guidance callout when no project is active
        st.info("💡 **Getting Started**: To upload documents, chat with them, or generate summaries, please select or create a project first.")
        
        col_guidance_1, col_guidance_2 = st.columns(2)
        with col_guidance_1:
            with st.container(border=True):
                st.markdown("### 📂 Create or Select Project")
                st.write("Organize your papers, notes, and AI chats by creating a project workspace.")
                if st.button("Manage Projects", use_container_width=True, type="primary"):
                    st.session_state.page = "Projects"
                    st.rerun()
        with col_guidance_2:
            with st.container(border=True):
                st.markdown("### ⚙️ Configure AI Settings")
                st.write("Switch between local models or connect your online NVIDIA AI Endpoints credentials.")
                if st.button("AI Settings", use_container_width=True):
                    st.session_state.page = "Settings"
                    st.rerun()