# src/embeddings/manager.py
import torch
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Returns the State-of-the-Art BAAI/bge-m3 model.
    Configured to run on NVIDIA GPU (RTX 3070).
    """
    # Check if GPU is actually available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Loading Embedding Model on: {device.upper()}")

    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True} 
    )