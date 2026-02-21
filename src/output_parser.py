import json
import re

def safe_parse_json(llm_response: str) -> dict:
    
    clean = re.sub(r"```(?:json)?", "", llm_response)
    clean = clean.replace("```", "").strip()
    
    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM output:\n{e}\n\nRaw output:\n{clean}")