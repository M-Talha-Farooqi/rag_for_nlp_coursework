import os
import shutil
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List
# --- FIX 1: Import the cleaning utility ---
from langchain_community.vectorstores.utils import filter_complex_metadata
from src.embeddings.manager import get_embedding_model

# Path where the DB will be saved on your Linux machine
DB_PATH = "data/vectordb"

def build_vector_store(chunks: List[Document]):
    """
    Takes text chunks, embeds them using BGE-M3, 
    and saves them to a persistent ChromaDB.
    """
    embeddings = get_embedding_model()
    
    # If DB exists, we might want to reset it for a clean build
    if os.path.exists(DB_PATH):
        print(f"🧹 Clearing old Vector DB at {DB_PATH}...")
        shutil.rmtree(DB_PATH)

    # --- FIX 2: Sanitize Metadata ---
    # ChromaDB crashes if metadata contains lists (like {'languages': ['eng']}).
    # This function converts those complex types into simple strings.
    print("🧹 Sanitizing metadata for ChromaDB...")
    clean_chunks = filter_complex_metadata(chunks)

    print(f"📦 Indexing {len(clean_chunks)} chunks into ChromaDB...")
    
    # Chroma handles saving automatically
    vectorstore = Chroma.from_documents(
        documents=clean_chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print(f"✅ ChromaDB successfully created at: {DB_PATH}")
    return vectorstore

def load_vector_store():
    """
    Loads the existing ChromaDB for retrieval.
    """
    embeddings = get_embedding_model()
    
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"❌ No DB found at {DB_PATH}. Run build script first!")
        
    return Chroma(
        persist_directory=DB_PATH, 
        embedding_function=embeddings
    )