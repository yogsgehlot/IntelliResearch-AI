import streamlit as st

from utils.session import logout


def render():

    col1, col2 = st.columns([8, 2])

    with col1:

        st.title("🧠 IntelliResearch AI")

        if st.session_state.project:
            st.caption(
                f"📂 Current Project: {st.session_state.project['name']}"
            )

    with col2:

        st.write("")  # small spacing

        if st.button(
            "Logout",
            use_container_width=True,
        ):
            logout()
            st.rerun()