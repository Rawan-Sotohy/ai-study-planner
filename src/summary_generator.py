import os
from langchain_groq import ChatGroq
from src.prompts import SUMMARY_PROMPT
from src.pdf_reader import load_vector_store
from src.config import GROQ_API_KEY, MODEL_NAME, SUMMARIES_PATH

def generate_summary(subject_name: str, topic_name: str) -> str:
    vector_store = load_vector_store(subject_name)
    docs = vector_store.similarity_search(topic_name, k=4)
    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME, temperature=0.3)
    chain = SUMMARY_PROMPT | llm

    response = chain.invoke({
        "topic_name": topic_name,
        "context": context
    })
    return response.content

def save_summary(subject_name: str, topic_name: str, summary: str):
    folder = f"{SUMMARIES_PATH}/{subject_name}"
    os.makedirs(folder, exist_ok=True)
    
    safe_name = topic_name.replace(" ", "_").replace("/", "-")
    file_path = f"{folder}/{safe_name}.txt"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Topic: {topic_name}\n")
        f.write("=" * 50 + "\n\n")
        f.write(summary)
    
    return file_path