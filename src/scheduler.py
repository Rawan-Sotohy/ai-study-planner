import json
from datetime import date, timedelta
from langchain_groq import ChatGroq
from src.prompts import SCHEDULE_PROMPT
from src.output_parser import safe_parse_json
from src.config import GROQ_API_KEY, MODEL_NAME

def calculate_available_days(exam_date: date) -> int:
    today = date.today()
    delta = (exam_date - today).days
    return max(delta, 1)

def generate_schedule(ranked_topics: list, exam_date: date,
                      daily_hours: int, subject_name: str, level: str) -> list:
    available_days = calculate_available_days(exam_date)

    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME, temperature=0.2)
    chain = SCHEDULE_PROMPT | llm

    response = chain.invoke({
        "topics_json": json.dumps(ranked_topics, indent=2),
        "available_days": available_days,
        "daily_hours": daily_hours,
        "level": level,
    })

    result = safe_parse_json(response.content)
    plan = result["plan"]

  
    today = date.today()
    for entry in plan:
        actual_date = today + timedelta(days=entry["day"] - 1)
        entry["date"] = actual_date.strftime("%Y-%m-%d")
        entry["subject"] = subject_name

    return plan