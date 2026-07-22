import streamlit as st

from services.chat import chat_service
from services.documents import document_service


def render():

    st.title("💬 AI Research Assistant")

    # Fetch and display uploaded files for single file chat selection
    docs = []
    try:
        doc_response = document_service.list(st.session_state.token)
        if doc_response.status_code == 200:
            docs = doc_response.json()
    except Exception:
        pass

    col1, col2 = st.columns([7, 3])

    with col1:
        # Filter dropdown
        doc_options = ["All Documents"] + [d["original_name"] for d in docs]
        selected_option = st.selectbox("Chat Focus / Single File Chat", options=doc_options)
        
        selected_doc_id = None
        if selected_option != "All Documents":
            for d in docs:
                if d["original_name"] == selected_option:
                    selected_doc_id = d["id"]
                    break

    with col2:
        st.write("")
        st.write("")
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.divider()
            
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
                question=question,
                document_id=selected_doc_id,
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