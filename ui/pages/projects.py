import streamlit as st

from services.projects import project_service

from components.project_card import project_card


def render():

    st.title("Projects")

    token = st.session_state.token

    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("Create Project")

        with st.form("create_project"):

            name = st.text_input("Project Name")

            description = st.text_area("Description")

            submit = st.form_submit_button(
                "Create Project"
            )

            if submit:

                response = project_service.create(
                    token,
                    name,
                    description,
                )

                if response.status_code in [200, 201]:

                    st.success(
                        "Project created."
                    )

                    st.rerun()

                else:

                    st.error(
                        response.text
                    )

    st.divider()

    st.subheader("Your Projects")

    response = project_service.list(
        token
    )

    if response.status_code != 200:

        st.error("Unable to load projects.")

        return

    projects = response.json()

    if not projects:

        st.info(
            "No projects yet."
        )

        return

    cols = st.columns(2)

    for index, project in enumerate(projects):

        with cols[index % 2]:

            project_card(project)