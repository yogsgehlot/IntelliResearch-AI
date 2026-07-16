import streamlit as st

from services.auth import auth_service
from utils.session import save_login

def render():

    # Center the login form
    left, center, right = st.columns([1.5, 2, 1.5])

    with center:

        st.markdown(
            """
            <div style="text-align:center;padding:20px 0 10px 0;">
                <h1>🧠 IntelliResearch AI</h1>
                <p style="color:gray;font-size:18px;">
                    Offline AI Research Assistant
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):

            st.subheader("Welcome Back")

            st.caption("Sign in to continue")

            email = st.text_input(
                "Email Address",
                placeholder="Enter your email",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
            )

            st.write("")

            if st.button(
                "🚀 Login",
                use_container_width=True,
                type="primary",
            ):

                if not email or not password:
                    st.warning("Please enter email and password.")
                    st.stop()

                with st.spinner("Signing in..."):

                    response = auth_service.login(
                        email,
                        password,
                    )

                if response.status_code == 200:

                    data = response.json()

                    save_login(
                        token=data["access_token"],
                        user=data.get("user"),
                    )

                    st.success("Login successful!")

                    st.rerun()

                else:

                    try:
                        detail = response.json().get(
                            "detail",
                            "Login failed.",
                        )
                    except Exception:
                        detail = response.text

                    st.error(detail)

            st.markdown("---")

            st.caption(
                "Powered by FastAPI • Ollama • FAISS • Streamlit"
            )