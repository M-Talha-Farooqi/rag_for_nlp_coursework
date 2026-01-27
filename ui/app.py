import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.layout import render_header, render_sidebar
from ui.session_state import init_session_state
from src.chains.rag_chain import build_rag_chain

st.set_page_config(page_title="NLP Assistant", page_icon="🧠", layout="wide")

def get_file_stats(raw_data_path):
    file_data = []
    if os.path.exists(raw_data_path):
        for root, dirs, files in os.walk(raw_data_path):
            for file in files:
                if not file.startswith('.'):
                    topic = os.path.basename(root)
                    file_data.append({"Topic": topic, "File Name": file, "Type": file.split('.')[-1].upper()})
    return file_data

def main():
    init_session_state()
    render_header()
    
    # 1. Get Settings (Provider, Model, Key Status)
    config = render_sidebar()
    
    # 2. Sidebar Inspector
    with st.sidebar:
        with st.expander("📂 Knowledge Inspector"):
            raw_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
            files = get_file_stats(raw_path)
            if files:
                df = pd.DataFrame(files)
                st.dataframe(df, hide_index=True)
                st.caption(f"Total Documents: {len(files)}")
            else:
                st.warning("No documents found.")

    # 3. Load Chain (Cached based on provider/model selection)
    @st.cache_resource(show_spinner="⚙️ Switching AI Brain...")
    def load_chain(prov, mod, temp, k):
        return build_rag_chain(provider=prov, model_name=mod, temperature=temp, k=k)

    # Only load if we have the key
    if config["has_key"]:
        try:
            st.session_state.rag_chain = load_chain(
                config["provider"], 
                config["model"], 
                config["temperature"], 
                config["k"]
            )
        except Exception as e:
            st.error(f"❌ Initialization Error: {e}")
            st.stop()
    else:
        st.warning("👈 Please enter an API Key in the sidebar to start.")
        st.stop()

    # FIX: Added [ ] around tab1 to unpack the single tab from the list
    [tab1] = st.tabs(["💬 Intelligent Chat"])

    with tab1:
        st.caption(f"Talking to: **{config['model']}**")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Enter your query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with tab1:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner(f"🧠 {config['provider']} is thinking..."):
                    try:
                        response = st.session_state.rag_chain.invoke({"input": prompt})
                        full_response = response.get("answer", "No response generated.")
                        message_placeholder.markdown(full_response)
                    except Exception as e:
                        full_response = f"⚠️ Error: {str(e)}"
                        message_placeholder.error(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()