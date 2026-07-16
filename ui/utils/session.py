import streamlit as st


def init_session():

    defaults = {
        "token": None,
        "user": None,
        "project": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


def is_authenticated():
    return st.session_state.token is not None


def logout():

    st.session_state.token = None
    st.session_state.user = None
    st.session_state.project = None