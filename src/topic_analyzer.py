import json
from langchain_groq import ChatGroq
from src.prompts import TOPIC_EXTRACTION_PROMPT
from src.output_parser import safe_parse_json
from src.pdf_reader import load_vector_store
from src.config import GROQ_API_KEY, MODEL_NAME, RETRIEVAL_K

def extract_topics(subject_name: str, level: str) -> list:
    
    vector_store = load_vector_store(subject_name)
    retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVAL_K})
    docs = retriever.invoke("main topics chapters units overview")
    syllabus_text = "\n\n".join([doc.page_content for doc in docs])

    
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME, temperature=0)
    chain = TOPIC_EXTRACTION_PROMPT | llm

    response = chain.invoke({
        "syllabus_text": syllabus_text,
        "level": level
    })

    result = safe_parse_json(response.content)
    return result["topics"]


def rank_topics(topics: list, level: str) -> list:
  
    if level == "Beginner":
       
        difficulty_order = {"Easy": 0, "Medium": 1, "Hard": 2}
    else:
        
        difficulty_order = {"Hard": 0, "Medium": 1, "Easy": 2}

    return sorted(topics, key=lambda t: difficulty_order.get(t["difficulty"], 99))