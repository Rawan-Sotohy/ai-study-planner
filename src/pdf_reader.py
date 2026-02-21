import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.config import VECTORSTORE_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def load_file(file_path: str) -> list:
    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        loader = PyPDFLoader(file_path)
    elif ext == "docx":
        loader = Docx2txtLoader(file_path)
    elif ext == "txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return loader.load()

def load_and_chunk_pdf(file_path: str) -> list:
    documents = load_file(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    return chunks

def create_vector_store(chunks: list, subject_name: str) -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_documents(chunks, embeddings)

    save_path = f"{VECTORSTORE_PATH}/{subject_name}"
    os.makedirs(save_path, exist_ok=True)
    vector_store.save_local(save_path)

    return vector_store

def load_vector_store(subject_name: str) -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    load_path = f"{VECTORSTORE_PATH}/{subject_name}"
    return FAISS.load_local(load_path, embeddings,
                            allow_dangerous_deserialization=True)