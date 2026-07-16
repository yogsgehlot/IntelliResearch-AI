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

    if not uploaded_files:
        return

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

                    st.error(
                        f"{file.name}\n{response.text}"
                    )

            progress.progress(
                (index + 1) / total
            )

        st.toast(
            "Documents uploaded successfully 🎉"
        )