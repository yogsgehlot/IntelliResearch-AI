import streamlit as st


def render():

    st.title("🏠 Dashboard")

    st.info(
        "Welcome to IntelliResearch AI"
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "📁 Projects",
            use_container_width=True,
        ):
            st.session_state.page = "Projects"

    with c2:

        if st.button(
            "📄 Upload Papers",
            use_container_width=True,
        ):
            st.session_state.page = "Upload"