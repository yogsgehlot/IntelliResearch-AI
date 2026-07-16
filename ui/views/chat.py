import streamlit as st

from services.chat import chat_service


def render():

    st.title("💬 AI Research Assistant")

    col1, col2 = st.columns([8, 2])

    with col2:

        if st.button("🗑 Clear Chat"):

            st.session_state.messages = []

            st.rerun()
            
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show history
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message.get("sources"):

                with st.expander("📚 Sources"):

                    for source in message["sources"]:
                        st.write(source)

    question = st.chat_input(
        "Ask about your documents..."
    )

    if not question:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = chat_service.ask(
                token=st.session_state.token,
                # project_id=st.session_state.project["id"],
                question=question,
            )

            if response.status_code != 200:

                st.error(response.text)

                return

            data = response.json()

            answer = data["answer"]

            sources = data.get(
                "sources",
                [],
            )

            st.markdown(answer)

            if sources:

                with st.expander("📚 Sources"):

                    for source in sources:

                        st.write(source)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                }
            )