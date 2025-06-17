# agents/rag_retriever.py

import os
from pathlib import Path
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain_core.documents import Document

def load_documents_with_fallback():
    try:
        file_path = Path(__file__).parent / "data" / "wcag_guidelines.txt"
        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")
        
        loader = TextLoader(str(file_path))
        return loader.load()
    except Exception as e:
        print(f"⚠️ Failed to load document. Using fallback. Error: {e}")
        # Fallback: In-memory document content
        fallback_text = """
        WCAG Alt Text Best Practices:
        - Be specific and concise (describe what the image conveys).
        - Avoid phrases like “image of” or “photo of”.
        - For decorative images, use empty alt: alt="".
        - For complex charts/graphs, include summaries nearby.
        - Alt text should serve the same purpose as the image.
        """
        return [Document(page_content=fallback_text)]

def setup_rag_agent():
    documents = load_documents_with_fallback()
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)

    retriever = db.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=retriever)
    return qa_chain

def fetch_best_practice(prompt):
    rag_agent = setup_rag_agent()
    return rag_agent.run(prompt)
