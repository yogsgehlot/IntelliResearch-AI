from streamlit_option_menu import option_menu
import streamlit as st


def render_sidebar():
    options = [
        "Dashboard",
        "Projects",
        "Upload",
        "Chat",
        "Summary",
        "Notes",
        "Settings",
    ]
    
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
        
    default_idx = 0
    if st.session_state.page in options:
        default_idx = options.index(st.session_state.page)

    with st.sidebar:
        st.title("🧠 IntelliResearch")

        if st.session_state.project:
            st.success(
                f"📂 {st.session_state.project['name']}"
            )
        else:
            st.info("No project selected")

        selected = option_menu(
            menu_title=None,
            options=options,
            icons=[
                "house",
                "folder",
                "cloud-upload",
                "chat-dots",
                "file-earmark-text",
                "journal-text",
                "gear",
            ],
            default_index=default_idx,
        )

    st.session_state.page = selected
    return selected