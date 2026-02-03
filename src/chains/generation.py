import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_llm(provider, model_name, temperature=0.0):
    """
    Factory function to return the selected LLM based on provider.
    """
    if provider == "Google Gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key: return None
        return ChatGoogleGenerativeAI(model=model_name, temperature=temperature, streaming=True, google_api_key=api_key)
    
    elif provider == "Groq (Llama 3)":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key: return None
        return ChatGroq(model=model_name, temperature=temperature, streaming=True, groq_api_key=api_key)

    elif provider == "OpenAI (GPT)":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key: return None
        return ChatOpenAI(model=model_name, temperature=temperature, streaming=True, api_key=api_key)
    
    return None