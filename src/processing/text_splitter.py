from typing import List
# --- FIX: Updated Import from 'langchain.schema' to 'langchain_core.documents' ---
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(
    docs: List[Document], 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Splits a list of Documents into smaller chunks.
    
    Args:
        docs: List of LangChain Documents (from the loader).
        chunk_size: Maximum characters per chunk (default 1000).
        chunk_overlap: How many characters to overlap between chunks (default 200).
                       Overlap ensures context isn't lost at the cut point.
    
    Returns:
        List[Document]: The list of smaller, chunked documents.
    """
    
    # 1. Configuration: "Smart" separators for technical content
    # We prioritize splitting by paragraphs (\n\n) -> lines (\n) -> spaces
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )

    print(f"✂️ Splitting {len(docs)} documents...")
    
    # 2. Execute Split
    # This automatically handles the metadata (Topic, Source) copying
    splits = text_splitter.split_documents(docs)
    
    print(f"✅ Generated {len(splits)} chunks from original documents.")
    
    return splits