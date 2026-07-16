import streamlit as st

from services.auth import auth_service


def render():

    st.title("🧠 IntelliResearch AI")

    st.subheader("Login")

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password",
    )

    if st.button(
        "Login",
        use_container_width=True,
    ):

        response = auth_service.login(
            email,
            password,
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.token = data["access_token"]

            st.session_state.user = data.get(
                "user",
            )

            st.success("Login successful")

            st.rerun()

        else:

            st.error(
                response.json().get(
                    "detail",
                    "Login failed",
                )
            )