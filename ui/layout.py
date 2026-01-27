import streamlit as st
import os
from src.utils.env_manager import save_key

def render_header():
    st.markdown("""<h1 style='text-align: center; color: #2E86C1;'>🧠 NLP Assistant <span style='font-size: 20px; color: #555;'></span></h1>""", unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=50)
        st.header("⚙️ Control Panel")
        
        # --- 1. PROVIDER SELECTION ---
        st.subheader("🤖 AI Brain")
        provider = st.selectbox(
            "Select Provider",
            ["Google Gemini", "Groq (Llama 3)", "OpenAI (GPT)"]
        )

        # --- 2. MODEL SELECTION (Updated with Real Groq Models) ---
        model_options = {
            "Google Gemini": [
                "gemini-2.0-flash",       # Newest Flash
                "gemini-1.5-pro",         # Smarter Pro
                "gemini-1.5-flash"        # Standard Flash
            ],
            "Groq (Llama 3)": [
                "llama-3.3-70b-versatile",         # 🌟 BEST (Smart & Fast)
                "llama-3.1-8b-instant",            # ⚡ FASTEST (Instant)
                "deepseek-r1-distill-llama-70b",   # 🧠 REASONING (DeepSeek)
                "mixtral-8x7b-32768"               # Good alternative
            ],
            "OpenAI (GPT)": [
                "gpt-4o-mini",
                "gpt-4o",
                "gpt-3.5-turbo"
            ]
        }
        selected_model = st.selectbox("Select Model", model_options[provider])

        # --- 3. API KEY CHECKER ---
        # Map provider to expected ENV variable name
        env_map = {
            "Google Gemini": "GOOGLE_API_KEY",
            "Groq (Llama 3)": "GROQ_API_KEY",
            "OpenAI (GPT)": "OPENAI_API_KEY"
        }
        required_key = env_map[provider]
        current_key = os.getenv(required_key)

        if not current_key:
            st.warning(f"⚠️ {required_key} is missing!")
            user_key = st.text_input(f"Enter {provider} API Key", type="password")
            if st.button("💾 Save API Key"):
                if user_key:
                    save_key(required_key, user_key)
                    st.success("Key Saved! Reloading...")
                    st.rerun()
        else:
            st.success(f"🔑 {provider} Connected")

        st.divider()
        
        # --- 4. PARAMETERS ---
        st.subheader("Parameters")
        temp = st.slider("Creativity", 0.0, 1.0, 0.0, 0.1)
        k_val = st.slider("Context Depth", 1, 10, 5)

        st.divider()
        st.subheader("System Status")
        st.info(f"🧠 {selected_model}") # <--- UPDATES DYNAMICALLY
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        return {
            "provider": provider,
            "model": selected_model,
            "temperature": temp,
            "k": k_val,
            "has_key": bool(current_key)
        }