import streamlit as st

def init_session_state():
    """
    Initializes session state variables for chat history.
    """
    # 1. Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. Initialize the Chain (Load only once to save time)
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None