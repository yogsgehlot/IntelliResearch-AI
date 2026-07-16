import streamlit as st
import extra_streamlit_components as stx

COOKIE_NAME = "intelliresearch_token"

cookie_manager = stx.CookieManager()


def init_session():

    defaults = {
        "token": None,
        "user": None,
        "project": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Restore token from cookie
    if st.session_state.token is None:
        token = cookie_manager.get(COOKIE_NAME)

        if token:
            st.session_state.token = token


def save_login(token, user=None):

    st.session_state.token = token
    st.session_state.user = user

    cookie_manager.set(
        COOKIE_NAME,
        token,
        expires_at=None,   # session cookie
    )


def is_authenticated():
    return st.session_state.token is not None


def logout():

    st.session_state.token = None
    st.session_state.user = None
    st.session_state.project = None

    cookie_manager.delete(COOKIE_NAME)