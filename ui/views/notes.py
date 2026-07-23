import streamlit as st

from services.notes import notes_service


def render():

    st.title("📒 Research Notes")

    project = st.session_state.project

    if project is None:
        st.warning("Please select a project.")
        return

    title = st.text_input("Title", placeholder="e.g. Key Takeaway on Laravel experience")
    note = st.text_area(
        "Write a note...",
        height=150,
    )

    if st.button(
        "Save Note",
        type="primary",
        use_container_width=True,
    ):
        if not title.strip() or not note.strip():
            st.error("Please fill in both the title and the content.")
        else:
            response = notes_service.create(
                st.session_state.token,
                project["id"],
                title,
                note,
            )

            if response.status_code in [200, 201]:
                st.success("Note saved.")
                st.rerun()
            else:
                st.error(response.text)

    st.divider()

    response = notes_service.list(
        st.session_state.token,
        project["id"],
    )

    if response.status_code != 200:
        st.error("Unable to load notes.")
        return

    notes = response.json()

    if not notes:
        st.info("No notes yet.")
        return

    for note in notes:
        with st.container(border=True):
            st.markdown(f"### 📌 {note.get('title', 'Untitled Note')}")
            st.markdown(note["content"])