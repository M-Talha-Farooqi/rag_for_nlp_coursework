from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from src.vectorstore.store import load_vector_store
from src.chains.generation import get_llm
from src.prompts.templates import get_chat_prompt

# FIX: Added provider and model_name arguments
def build_rag_chain(provider, model_name, temperature=0.0, k=5):
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    
    # FIX: Get the specific LLM requested
    llm = get_llm(provider, model_name, temperature)
    
    if llm is None:
        raise ValueError(f"❌ Missing API Key for {provider}")

    main_prompt = get_chat_prompt()
    document_prompt = PromptTemplate.from_template("Content: {page_content}\nSource: {source_filename}")
    
    question_answer_chain = create_stuff_documents_chain(llm, main_prompt, document_prompt=document_prompt, document_variable_name="context")
    return create_retrieval_chain(retriever, question_answer_chain)