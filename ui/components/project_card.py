import streamlit as st


def project_card(project):

    with st.container(border=True):

        st.subheader(project["name"])

        st.caption(project["description"])

        if st.button(
            "Open",
            key=project["id"],
            use_container_width=True,
        ):

            st.session_state.project = project

            st.success(
                f'Selected "{project["name"]}"'
            )

            st.rerun()