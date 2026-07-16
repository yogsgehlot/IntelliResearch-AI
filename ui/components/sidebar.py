from streamlit_option_menu import option_menu
import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("🧠 IntelliResearch AI")

        if st.session_state.project:
            st.success(
                f"📂 {st.session_state.project['name']}"
            )
        else:
            st.info("No project selected")

        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Projects",
                "Upload",
                "Chat",
                "Summary",
                "Notes",
                "Settings",
            ],
            icons=[
                "house",
                "folder",
                "cloud-upload",
                "chat-dots",
                "file-earmark-text",
                "journal-text",
                "gear",
            ],
            default_index=0,
        )

    return selected