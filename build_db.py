import sys
import os

# 1. Setup System Path so Python can find 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# 2. Import our Modules
from src.ingestion.loader_factory import load_documents_from_folder
from src.processing.text_splitter import split_documents
from src.vectorstore.store import build_vector_store

def main():
    print("🚀 Starting RAG Pipeline Construction...")

    # --- Step 1: Ingestion ---
    # We point to "data/raw/Final NLP" because that is where you uploaded your folders
    raw_data_path = os.path.join("data", "raw")
    
    if not os.path.exists(raw_data_path):
        print(f"❌ Error: The folder '{raw_data_path}' does not exist.")
        print("   Did you upload 'Final NLP' to 'data/raw' correctly?")
        return

    docs = load_documents_from_folder(raw_data_path)
    
    if not docs:
        print("⚠️ Warning: No documents were found!")
        return

    # --- Step 2: Splitting ---
    # The splitter uses the logic from src/processing/text_splitter.py
    chunks = split_documents(docs)

    # --- Step 3: Vectorization & Storage ---
    # This uses BGE-M3 (GPU) and saves to ChromaDB
    build_vector_store(chunks)

    print("\n🎉 SUCCESS: Database built successfully!")
    print(f"   Total Documents Processed: {len(docs)}")
    print(f"   Total Searchable Chunks: {len(chunks)}")

if __name__ == "__main__":
    main()