import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.config import *

def load_and_chunk_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    return splitter.split_documents(docs)

def create_vector_store(chunks, subject_name):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    path = f"{VECTORSTORE_PATH}/{subject_name}"
    os.makedirs(path, exist_ok=True)
    vectorstore.save_local(path)

def load_vector_store(subject_name):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    path = f"{VECTORSTORE_PATH}/{subject_name}"
    return FAISS.load_local(path, embeddings,
                            allow_dangerous_deserialization=True)
