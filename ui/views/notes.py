import streamlit as st

from services.notes import notes_service


def render():

    st.title("📒 Research Notes")

    project = st.session_state.project

    if project is None:
        st.warning("Please select a project.")
        return

    note = st.text_area(
        "Write a note...",
        height=150,
    )

    if st.button(
        "Save Note",
        type="primary",
        use_container_width=True,
    ):

        response = notes_service.create(
            st.session_state.token,
            project["id"],
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

            st.markdown(note["content"])