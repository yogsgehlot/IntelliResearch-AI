import streamlit as st
from services.summary import summary_service

def render():
    st.title("📄 Research Summary")
    
    project = st.session_state.project
    if project is None:
        st.warning("Please select a project first.")
        return

    st.subheader(f"Generate Summary for {project['name']}")
    
    with st.form("generate_summary_form"):
        topic = st.text_input("Summary Topic / Focus (e.g. key takeaways, methodology, results)", value="General Overview")
        summary_type = st.selectbox(
            "Summary Type",
            options=["project_summary", "executive_summary", "methodology_review", "findings_synthesis"],
            format_func=lambda x: x.replace("_", " ").title()
        )
        submit = st.form_submit_button("Generate Summary", type="primary")

    if submit:
        with st.spinner("Synthesizing document contents and generating summary..."):
            response = summary_service.generate(
                st.session_state.token,
                project["id"],
                topic,
                summary_type
            )
            
            if response.status_code in [200, 201]:
                st.success("Summary generated successfully!")
                st.rerun()
            else:
                st.error(f"Failed to generate summary: {response.text}")

    st.divider()
    st.subheader("Current Project Summary")

    with st.spinner("Loading summary..."):
        response = summary_service.get(st.session_state.token, project["id"])
        
        if response.status_code == 200:
            summary = response.json()
            if summary:
                # Backend returns list or single summary object. 
                # Let's inspect response structure. If it's a list:
                if isinstance(summary, list):
                    if not summary:
                        st.info("No summary generated yet. Use the form above to generate one.")
                    for item in summary:
                        render_single_summary(item, project["id"])
                else:
                    render_single_summary(summary, project["id"])
            else:
                st.info("No summary generated yet. Use the form above to generate one.")
        else:
            st.info("No summary generated yet. Use the form above to generate one.")

def render_single_summary(summary, project_id):
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### 📌 {summary.get('topic', 'Summary')}")
            st.caption(f"Type: {summary.get('summary_type', '').replace('_', ' ').title()} | Created at: {summary.get('created_at', '')[:19].replace('T', ' ')}")
        with col2:
            if st.button("Delete", key=f"del_{summary.get('id')}", type="secondary"):
                with st.spinner("Deleting..."):
                    del_response = summary_service.delete(st.session_state.token, project_id)
                    if del_response.status_code in [200, 204]:
                        st.success("Deleted successfully.")
                        st.rerun()
                    else:
                        st.error("Failed to delete summary.")
                        
        st.markdown(summary.get("content", ""))
