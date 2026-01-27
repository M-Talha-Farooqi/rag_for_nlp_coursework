import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    Docx2txtLoader,
    TextLoader,
    PyPDFLoader
)
from src.ingestion.custom_loaders import CleanNotebookLoader
# FIX: Import our new robust loader
from src.ingestion.pptx_loader import RobustPPTXLoader 

def get_loader(file_path: str):
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension == ".pptx":
        # FIX: Switch to the robust loader
        return RobustPPTXLoader(file_path)
    
    elif extension == ".docx":
        return Docx2txtLoader(file_path)
    
    elif extension == ".pdf":
        return PyPDFLoader(file_path)
    
    elif extension == ".ipynb":
        return CleanNotebookLoader(file_path)
    
    elif extension == ".txt":
        return TextLoader(file_path)
    
    else:
        return None

def load_documents_from_folder(root_dir: str) -> List[Document]:
    all_documents = []
    print(f"📂 Scanning directory: {root_dir}")

    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            loader = get_loader(file_path)
            
            if loader:
                try:
                    # Robust loader doesn't print internal logs, so we print here
                    # print(f"   Processing: {file}...") 
                    raw_docs = loader.load()
                    
                    topic = os.path.basename(dirpath)
                    for doc in raw_docs:
                        doc.metadata["source_filename"] = file
                        doc.metadata["topic"] = topic
                        if "source" not in doc.metadata:
                            doc.metadata["source"] = file_path
                    
                    all_documents.extend(raw_docs)
                except Exception as e:
                    print(f"❌ Error processing {file}: {str(e)}")
            else:
                continue

    print(f"✅ Loaded {len(all_documents)} document chunks from {root_dir}")
    return all_documents