# agents/rag_retriever.py
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def setup_rag_agent():
    loader = TextLoader("data/wcag_guidelines.txt")
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)

    retriever = db.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=retriever)
    return qa_chain

def fetch_best_practice(prompt):
    rag_agent = setup_rag_agent()
    return rag_agent.run(prompt)
