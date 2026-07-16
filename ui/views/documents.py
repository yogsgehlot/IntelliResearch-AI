import streamlit as st

from services.documents import document_service


def render():

    if not st.session_state.project:

        st.warning(
            "Please select a project first."
        )

        return

    st.title("Upload Documents")

    uploaded = st.file_uploader(
        "Upload Research Papers",
        type=[
            "pdf",
            "docx",
            "txt",
            "png",
            "jpg",
            "jpeg",
        ],
        accept_multiple_files=True,
    )

    if uploaded:

        token = st.session_state.token

        project = st.session_state.project

        for file in uploaded:
            progress = st.progress(0)

            total = len(uploaded)

            with st.spinner(
                f"Uploading {file.name}..."
            ):

                response = document_service.upload(
                    token,
                    project["id"],
                    file,
                )

                if response.status_code in [200, 201]:

                    st.success(
                        f"{file.name} uploaded."
                    )

                else:

                    st.error(
                        response.text
                    )
            
            progress.progress((index + 1) / total)