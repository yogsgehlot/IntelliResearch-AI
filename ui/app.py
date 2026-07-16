import streamlit as st

from utils.session import (
    init_session,
    is_authenticated,
)

from pages.login import render as login_page

from pages.dashboard import render as dashboard_page

from components.sidebar import render_sidebar

from components.header import render as header
from pages.projects import render as projects_page
from pages.upload import render as upload_page
from pages.chat import render as chat_page
from pages.notes import render as notes_page

init_session()

st.set_page_config(
    page_title="IntelliResearch AI",
    layout="wide",
)

if not is_authenticated():

    login_page()

    st.stop()

header()

page = render_sidebar()

if page == "Dashboard":

    dashboard_page()

elif page == "Projects":

    projects_page()

elif page == "Upload":

    upload_page()

elif page == "Chat":
    chat_page()

elif page == "Summary":

    st.header("Summary")

elif page == "Notes":

    notes_page()

elif page == "Settings":

    st.header("Settings")