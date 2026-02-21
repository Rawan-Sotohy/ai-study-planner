from langchain_core.prompts import PromptTemplate

TOPIC_EXTRACTION_PROMPT = PromptTemplate(
    input_variables=["syllabus_text", "level"],
    template="""
You are an expert academic curriculum analyzer.

Below is a syllabus excerpt for a student at the {level} level.
Extract a list of key study topics. For each topic provide:
- topic_name
- difficulty (Easy / Medium / Hard)
- estimated_hours (how many hours to study it)
- description (one sentence)

Return ONLY valid JSON like this, no extra text:
{{
  "topics": [
    {{"topic_name": "...", "difficulty": "...", "estimated_hours": 2, "description": "..."}}
  ]
}}

Syllabus text:
{syllabus_text}
"""
)

SCHEDULE_PROMPT = PromptTemplate(
    input_variables=["topics_json", "available_days", "daily_hours", "level"],
    template="""
You are a smart study planner.

Student level: {level}
Available days until exam: {available_days}
Daily study hours: {daily_hours}

Topics to cover (JSON):
{topics_json}

Create a daily study plan. Rules:
- Prioritize harder topics earlier
- Last 2 days are always Revision only
- Mix study types: Reading, Practice, Revision
- Fit topics within available days and daily hours

Return ONLY valid JSON, no extra text:
{{
  "plan": [
    {{"day": 1, "subject": "...", "topic": "...", "study_type": "...", "duration_hours": 1.5}}
  ]
}}
"""
)

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["topic_name", "context"],
    template="""
Write a clear and concise study summary for the topic: "{topic_name}".
Use the following source material:
{context}

The summary should be:
- 3 to 5 paragraphs
- Student friendly
- Highlight key points

Summary:
"""
)