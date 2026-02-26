import json
from langchain_groq import ChatGroq
from pdf_reader import load_vector_store
from config import *
from datetime import date

def extract_topics(subject_name: str, level: str):

    vector_store = load_vector_store(subject_name)
    retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVAL_K})
    docs = retriever.invoke("Main chapters and topics overview")

    syllabus_text = "\n\n".join([d.page_content for d in docs])

    
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0
    ).bind(response_format={"type": "json_object"}) 

    prompt = f"""
Extract key study topics from this syllabus.

For each topic return:
- topic_name
- difficulty (Easy/Medium/Hard)
- estimated_hours (number)

Return ONLY a valid JSON object with the key "topics".

Student level: {level}

Syllabus:
{syllabus_text}
"""

    response = llm.invoke(prompt)
    result = json.loads(response.content)

    return result["topics"]
