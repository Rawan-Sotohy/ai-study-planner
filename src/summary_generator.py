from langchain_groq import ChatGroq
from src.pdf_reader import load_vector_store
from src.config import *
import os

def generate_summary(subject_name, topic_name):

    vector_store = load_vector_store(subject_name)
    docs = vector_store.similarity_search(topic_name, k=5)
    context = "\n\n".join([d.page_content for d in docs])

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0.3
    )

    prompt = f"""
Write a structured revision summary for:

{topic_name}

Based on:
{context}

Make it clear, exam-focused, and concise.
"""

    return llm.invoke(prompt).content

def save_summary(summary_text, subject_name, topic_name):
    
    subject_folder = os.path.join(OUTPUTS_PATH, subject_name.replace(" ", "_"))
    os.makedirs(subject_folder, exist_ok=True)
    
    
    clean_topic = "".join(c for c in topic_name if c.isalnum() or c in (' ', '_')).strip()
    clean_topic = clean_topic[:50]
    
    file_name = f"{clean_topic}_summary.txt".replace(" ", "_")
    file_path = os.path.join(subject_folder, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(summary_text)
    
    return file_path
