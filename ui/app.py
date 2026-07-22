import streamlit as st

from utils.session import (
    init_session,
    is_authenticated,
)

from views.login import render as login_page

from views.dashboard import render as dashboard_page

from components.sidebar import render_sidebar

from components.header import render as header
from views.projects import render as projects_page
from views.upload import render as upload_page
from views.chat import render as chat_page
from views.notes import render as notes_page
from views.summary import render as summary_page
from views.settings import render as settings_page

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

    summary_page()

elif page == "Notes":

    notes_page()

elif page == "Settings":

    settings_page()