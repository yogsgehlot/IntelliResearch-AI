import streamlit as st
from services.documents import document_service

def render():
    st.title("📄 Upload Research Papers")

    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=[
            "pdf",
            "docx",
            "txt",
            "png",
            "jpg",
            "jpeg",
        ],
    )

    if uploaded_files:
        if st.button(
            "Upload Documents",
            type="primary",
            use_container_width=True,
        ):
            progress = st.progress(0)
            total = len(uploaded_files)
            for index, file in enumerate(uploaded_files):
                with st.spinner(f"Uploading {file.name}..."):
                    response = document_service.upload(
                        st.session_state.token,
                        file,
                    )
                    if response.status_code in [200, 201]:
                        st.success(f"✅ {file.name}")
                    else:
                        st.error(f"{file.name}\n{response.text}")
                progress.progress((index + 1) / total)
            st.toast("Documents uploaded successfully 🎉")
            st.rerun()

    st.divider()
    st.subheader("Uploaded Documents & Processing Status")
    
    try:
        response = document_service.list(st.session_state.token)
        if response.status_code == 200:
            docs = response.json()
            if not docs:
                st.info("No documents uploaded yet.")
            else:
                for doc in docs:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([5, 2, 2])
                        with col1:
                            st.markdown(f"**📄 {doc['original_name']}**")
                            size_mb = doc['file_size'] / (1024 * 1024)
                            st.caption(f"Size: {size_mb:.2f} MB")
                        with col2:
                            status = doc['status']
                            if status == "READY":
                                st.success("Ready")
                            elif status == "PROCESSING":
                                st.warning("Processing...")
                            elif status == "FAILED":
                                st.error("Failed")
                            else:
                                st.info(status)
                        with col3:
                            # Auto refresh helper
                            if status == "PROCESSING":
                                if st.button("🔄 Refresh Status", key=f"ref_{doc['id']}"):
                                    st.rerun()
        else:
            st.error("Failed to load uploaded documents.")
    except Exception as e:
        st.error(f"Error connecting to server: {e}")