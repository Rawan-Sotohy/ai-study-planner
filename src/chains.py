from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, MODEL_NAME
from src.prompts import TOPIC_EXTRACTION_PROMPT, SCHEDULE_PROMPT, SUMMARY_PROMPT

def get_llm(temperature: float = 0):
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=temperature
    )

def get_topic_extraction_chain():
    llm = get_llm(temperature=0)
    return TOPIC_EXTRACTION_PROMPT | llm

def get_schedule_chain():
    llm = get_llm(temperature=0.2)
    return SCHEDULE_PROMPT | llm

def get_summary_chain():
    llm = get_llm(temperature=0.3)
    return SUMMARY_PROMPT | llm